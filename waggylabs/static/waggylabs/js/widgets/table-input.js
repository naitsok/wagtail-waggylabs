
/**
 * Function to initialize Handsontable
 * @param {string} id - id of the element that contains the value to be displayed in the table
 * @param {object} tableOptions - options for the table
 */
function initTable(id, tableOptions) {
    const containerId = id + '-handsontable-container';
    const tableHeaderCheckboxId = id + '-handsontable-header';
    const colHeaderCheckboxId = id + '-handsontable-col-header';
    const tableCaptionId = id + '-handsontable-col-caption';
    const hiddenStreamInput = $('#' + id);
    const tableHeaderCheckbox = $('#' + tableHeaderCheckboxId);
    const colHeaderCheckbox = $('#' + colHeaderCheckboxId);
    const tableCaption = $('#' + tableCaptionId);
    const finalOptions = {};
    let hot = null;
    let dataForForm = null;
    let isInitialized = false;

    const getWidth = () => {
        return $('.widget-table_input').closest('.sequence-member-inner').width();
    };
    const getHeight = () => {
        const tableParent = $('#' + id).parent();
        return tableParent.find('.htCore').height() + (tableParent.find('.input').height() * 2);
    };
    const resizeTargets = ['.input > .handsontable', '.wtHider', '.wtHolder'];
    const resizeHeight = (height) => {
        const currTable = $('#' + id);
        $.each(resizeTargets, () => {
            currTable.closest('.field-content').find(this).height(height);
        });
    };
    function resizeWidth(width) {
        $.each(resizeTargets, () => {
            $(this).width(width);
        });
        const parentDiv = $('.widget-table_input').parent();
        parentDiv.find('.field-content').width(width);
        parentDiv.find('.fieldname-table .field-content .field-content').width('80%');
    }

    try {
        dataForForm = JSON.parse(hiddenStreamInput.val());
    } catch (e) {
        // do nothing
    }

    if (dataForForm !== null) {
        if (dataForForm.hasOwnProperty('first_row_is_table_header')) {
            tableHeaderCheckbox.prop('checked', dataForForm.first_row_is_table_header);
        }
        if (dataForForm.hasOwnProperty('first_col_is_header')) {
            colHeaderCheckbox.prop('checked', dataForForm.first_col_is_header);
        }
        if (dataForForm.hasOwnProperty('table_caption')) {
            tableCaption.prop('value', dataForForm.table_caption);
        }
    }

    if (!tableOptions.hasOwnProperty('width') || !tableOptions.hasOwnProperty('height')) {
        // Size to parent .sequence-member-inner width if width is not given in tableOptions
        $(window).on('resize', () => {
            hot.updateSettings({
                width: getWidth(),
                height: getHeight()
            });
            resizeWidth('100%');
        });
    }

    const getCellsClassnames = () => {
        const meta = hot.getCellsMeta();
        const cellsClassnames = [];
        for (let i = 0; i < meta.length; i++) {
            if (meta[i].hasOwnProperty('className')) {
                cellsClassnames.push({
                    row: meta[i].row,
                    col: meta[i].col,
                    className: meta[i].className
                });
            }
        }
        return cellsClassnames;
    };

    const typesetOnLoad = () => {
        var data = hot.getData();
        for (let row in data) {
            for (let col in data[row]) {
                var cell = hot.getCell(row, col);
                if (data[row][col] && cell) {
                    MathJax.typesetClear([cell]);
                    // removal of <p></p> elemens is needed for correct display of cell data
                    cell.innerHTML = renderMarkdown(data[row][col], {}).replace(/\<p\>/g, "").replace(/\<\/p\>/g, "");
                    try {
                        MathJax.typeset([cell]);
                    }
                    catch (error) {
                        console.error("MathJax error in table cell which does not prevent functioning\n" + error);
                    }
                }
            }
        }
    }

    const typesetCell = (cell, row, col, prop, value, cellProps) => {
        if (hot && MathJax && MathJax.typesetClear && MathJax.typeset ) {
            MathJax.typesetClear([cell]);
            if (value) {
                // removal of <p></p> elemens is needed for correct display of cell data
                cell.innerHTML = renderMarkdown(value, {}).replace(/\<p\>/g, "").replace(/\<\/p\>/g, "");
                try {
                    MathJax.typeset([cell]);
                }
                catch (error) {
                    console.error("MathJax error in table cell which does not prevent functioning\n" + error);
                }
            }
        }
    }

    const persist = () => {
        hiddenStreamInput.val(JSON.stringify({
            data: hot.getData(),
            cell: getCellsClassnames(),
            first_row_is_table_header: tableHeaderCheckbox.prop('checked'),
            first_col_is_header: colHeaderCheckbox.prop('checked'),
            table_caption: tableCaption.val()
        }));
    };

    const cellEvent = (change, source) => {
        if (source === 'loadData') {
            return;  // don't save this change
        }
        persist();
    };

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const metaEvent = (row, column, key, value) => {
        if (isInitialized && key === 'className') {
            persist();
        }
    };

    const initEvent = () => {
        isInitialized = true;
    };

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const structureEvent = (index, amount) => {
        persist();
    };

    tableHeaderCheckbox.on('change', () => {
        persist();
    });

    colHeaderCheckbox.on('change', () => {
        persist();
    });

    tableCaption.on('change', () => {
        persist();
    });

    const defaultOptions = {
        afterChange: cellEvent,
        afterCreateCol: structureEvent,
        afterCreateRow: structureEvent,
        afterRemoveCol: structureEvent,
        afterRemoveRow: structureEvent,
        afterSetCellMeta: metaEvent,
        afterInit: initEvent,
        afterRenderer: typesetCell,
        // contextMenu set via init, from server defaults
    };

    if (dataForForm !== null) {
        // Overrides default value from tableOptions (if given) with value from database
        if (dataForForm.hasOwnProperty('data')) {
            defaultOptions.data = dataForForm.data;
        }
        if (dataForForm.hasOwnProperty('cell')) {
            defaultOptions.cell = dataForForm.cell;
        }
    }

    Object.keys(defaultOptions).forEach((key) => {
        finalOptions[key] = defaultOptions[key];
    });
    Object.keys(tableOptions).forEach((key) => {
        finalOptions[key] = tableOptions[key];
    });

    hot = new Handsontable(document.getElementById(containerId), finalOptions);
    hot.render(); // Call to render removes 'null' literals from empty cells
    // $(document).ready(function() {
    //   typesetOnLoad();
    // });
    

    // Apply resize after document is finished loading (parent .sequence-member-inner width is set)
    if ('resize' in $(window)) {
        resizeHeight(getHeight());
        $(window).on('load', () => {
            $(window).trigger('resize');
        });
    }
}