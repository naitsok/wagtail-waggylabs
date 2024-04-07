
/**
 * Due to the limitations of Handsontable, the 'cell' elements do not accept keyboard focus.
 * To achieve this we will convert each cell to contenteditable with plaintext (for browsers that support this).
 * This is not a perfect fix, clicking in a cell and then using keyboard has some quirks.
 * However, without these attributes the keyboard cannot navigate to edit these cells at a..
 */
const keyboardAccessAttrs = {
    'contenteditable': 'true',
    'plaintext-only': 'true',
    'tabindex': '0',
};

/**
 * Function to initialize Handsontable
 * @param {string} id - id of the element that contains the value to be displayed in the table
 * @param {object} tableOptions - options for the table
 */
function initTable(id, tableOptions) {
    const containerId = id + '-handsontable-container';
    const tableHeaderId = id + '-handsontable-header';
    const colHeaderId = id + '-handsontable-col-header';
    const headerChoiceId = id + '-table-header-choice';
    const tableCaptionId = id + '-handsontable-col-caption';
    const hiddenStreamInput = $('#' + id);
    var tableHeader = $('#' + tableHeaderId);
    var colHeader = $('#' + colHeaderId);
    var headerChoice = $('#' + headerChoiceId);
    const tableCaption = $('#' + tableCaptionId);
    const tableParent = $('#' + id).parent();
    // Attempt to get rid of JQuery - not needed now
    // const hiddenStreamInput = document.getElementById(id);
    // const tableHeader = document.getElementById(tableHeaderId);
    // const colHeader = document.getElementById(colHeaderId);
    // const headerChoice = document.getElementById(headerChoiceId);
    // const tableCaption = document.getElementById(tableCaptionId);
    // const tableParent = hiddenStreamInput.parentElement;
    const finalOptions = {};
    let hot = null;
    let dataForForm = null;
    let isInitialized = false;

    function closest(element, selector) {
        // alternative to JQuery closest()
        while (element && !element.matches(selector)) {
            element = element.parentElement;
        }
        return element;
    };
    const getWidth = () => {
        return $('.w-field--table_input').closest('.w-panel').width();
    };
    const getHeight = () => {
        let htCoreHeight = 0;
        tableParent.find('.htCore').each(function() {
            htCoreHeight += $(this).height();
        });
        return htCoreHeight + tableParent.find('[data-field]').first().height();
        // Attempt to get rid of JQuery - not needed now
        // tableParent.querySelectorAll('.htCore').forEach(() => {
        //     htCoreHeight += $(this).height();
        // });
        // return htCoreHeight + tableParent.querySelectorAll('[data-field]')[0].clientHeight;
    };
    const resizeTargets = [`#${containerId}`, '.wtHider', '.wtHolder'];
    const resizeHeight = (height) => {
        const currTable = $('#' + id);
        $.each(resizeTargets, function() {
            currTable.closest('[data-field]').find(this).height(height);
        });
    };
    function resizeWidth(width) {
        $.each(resizeTargets, function() {
            $(this).width(width);
        });
        const field = $('.w-field--table_input');
        field.width(width);
    }

    try {
        dataForForm = JSON.parse(hiddenStreamInput.val());
        // dataForForm = JSON.parse(hiddenStreamInput.value);
    } catch (e) {
        // do nothing
    }

    if (dataForForm !== null) {
        if (dataForForm.hasOwnProperty('table_caption')) {
            tableCaption.prop('value', dataForForm.table_caption);
            // tableCaption.value = dataForForm.table_caption;
        }
        if (dataForForm.hasOwnProperty('table_header_choice')) {
            headerChoice.prop('value', dataForForm.table_header_choice);
            // headerChoice.value = dataForForm.table_header_choice;
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

    // not needed anymore - see persist()
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

        const cell = [];
        const mergeCells = [];
        const cellsMeta = hot.getCellsMeta();

        cellsMeta.forEach((meta) => {
            let className;
            let hidden;

            if (meta.hasOwnProperty('className')) {
                className = meta.className;
            }
            if (meta.hasOwnProperty('hidden')) {
                // Cells are hidden if they have been merged
                hidden = true;
            }

            // Undefined values won't be included in the output
            if (className !== undefined || hidden) {
                cell.push({
                    row: meta.row,
                    col: meta.col,
                    className: className,
                    hidden: hidden,
                });
            }
        });

        if (hot.getPlugin('mergeCells').isEnabled()) {
        const collection = hot.getPlugin('mergeCells').mergedCellsCollection;

        collection.mergedCells.forEach((merge) => {
            mergeCells.push({
                row: merge.row,
                col: merge.col,
                rowspan: merge.rowspan,
                colspan: merge.colspan,
            });
        });
        }

        hiddenStreamInput.val(JSON.stringify({
                data: hot.getData(),
                cell: cell,
                mergeCells: mergeCells,
                first_row_is_table_header: tableHeader.val(),
                first_col_is_header: colHeader.val(),
                table_header_choice: headerChoice.val(),
                table_caption: tableCaption.val(),
            }),
        );
    };

    const cellEvent = (change, source) => {
        if (!isInitialized || source === 'loadData' || source === 'MergeCells') {
            return; // don't save this change
        }
        persist();
    };

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const metaEvent = (row, column, key, value) => {
        if (isInitialized && key === 'className') {
            persist();
        }
    };

    const mergeEvent = (cellRange, mergeParent, auto) => {
        if (isInitialized) {
            persist();
        }
    };

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const unmergeEvent = function (cellRange, auto) {
        if (isInitialized) {
            persist();
        }
    };

    const initEvent = () => {
        isInitialized = true;
    };

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const structureEvent = (index, amount) => {
        // resizeHeight(getHeight());
        persist();
        // wait until the document is ready and add these attributes.
        $(() => {
            $(tableParent).find('td, th').attr(keyboardAccessAttrs);
            // window resize event is able to trigger table resize, other methods such as above
            // resizeHeight() does not seem to work
            window.dispatchEvent(new Event('resize'));
        });
    };

    headerChoice.on('change', () => { // addEventListener
        persist();
    });
    
    tableCaption.on('change', () => { // addEventListener
        persist();
    });

    const defaultOptions = {
        afterChange: cellEvent,
        afterCreateCol: structureEvent,
        afterCreateRow: structureEvent,
        afterRemoveCol: structureEvent,
        afterRemoveRow: structureEvent,
        afterSetCellMeta: metaEvent,
        afterMergeCells: mergeEvent,
        afterUnmergeCells: unmergeEvent,
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

    if (finalOptions.hasOwnProperty('mergeCells') && finalOptions.mergeCells === true) {
        // If mergeCells is enabled and true then use the value from the database
        if (dataForForm !== null && dataForForm.hasOwnProperty('mergeCells')) {
            finalOptions.mergeCells = dataForForm.mergeCells;
        }
    }

    hot = new Handsontable(document.getElementById(containerId), finalOptions);
    window.addEventListener('load', () => {
        // Render the table. Calling render also removes 'null' literals from empty cells.
        hot.render();
        resizeHeight(getHeight());
        tableParent.find('td, th').attr(keyboardAccessAttrs);
        window.dispatchEvent(new Event('resize'));
    });

}