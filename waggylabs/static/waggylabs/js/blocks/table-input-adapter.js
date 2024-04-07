/**
 * Telepath adapter for the Handsontable table block.
*/
(() => {

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

    class TableInput {
        constructor(options, strings) {
            this.options = options;
            this.strings = strings;
        }

        render(placeholder, name, id, initialState) {
            const container = document.createElement('div');
            container.innerHTML = `
                <div class="w-field__wrapper" data-field-wrapper>
                    <label class="w-field__label" for="${id}-table-header-choice">${this.strings['Table headers']}</label>
                        <select id="${id}-table-header-choice" name="table-header-choice">
                            <option value="">Select a header option</option>
                            <option value="row">
                                ${this.strings['Display the first row as a header']}
                            </option>
                            <option value="column">
                                ${this.strings['Display the first column as a header']}
                            </option>
                            <option value="both">
                                ${this.strings['Display the first row AND first column as headers']}
                            </option>
                            <option value="neither">
                                ${this.strings['No headers']}
                            </option>
                        </select>
                    <p class="help">${this.strings['Which cells should be displayed as headers?']}</p>
                </div>
                <div class="w-field__wrapper" style="display:none;" data-field-wrapper>
                    <label class="w-field__label" for="${id}-handsontable-col-caption">${this.strings['Table caption']}</label>
                    <div class="w-field w-field--char_field w-field--text_input" data-field>
                        <div class="w-field__help" id="${id}-handsontable-col-caption-helptext" data-field-help>
                            <div class="help">${this.strings['A heading that identifies the overall topic of the table, and is useful for screen reader users.']}</div>
                        </div>
                        <div class="w-field__input" data-field-input>
                            <input type="text" id="${id}-handsontable-col-caption" name="handsontable-col-caption" aria-describedby="${id}-handsontable-col-caption-helptext" />
                        </div>
                    </div>
                </div>
                <div id="${id}-handsontable-container"></div>
                <input type="hidden" name="${name}" id="${id}" placeholder="${this.strings['Table']}">
            `;
            // Modification from default innerHTML: style="display:none;" at line 46 since the table caption is a separate Markdown block
            placeholder.replaceWith(container);

            const input = container.querySelector(`input[name="${name}"]`);
            const options = this.options;

            const widget = {
                getValue() {
                    return JSON.parse(input.value);
                },
                getState() {
                    return JSON.parse(input.value);
                },
                setState(state) {
                    input.value = JSON.stringify(state);
                    initTable(id, options);
                },
                // eslint-disable-next-line @typescript-eslint/no-empty-function
                focus() {},
            };
            widget.setState(initialState);
            return widget;
        }
    }
    window.telepath.register('waggylabs.widgets.TableInput', TableInput);
})();