/**
 * Telepath adapter for the Handsontable table block.
*/
(() => {
    class TableInput {
        constructor(options, strings) {
            this.options = options;
            this.strings = strings;
        }

        render(placeholder, name, id, initialState) {
            const container = document.createElement('div');
            container.innerHTML = `
              <div class="field boolean_field widget-checkbox_input">
                <div class="field-content">
                  <div class="input">
                    <input type="checkbox" id="${id}-handsontable-header" name="handsontable-header" />
                    <label for="${id}-handsontable-header"> ${this.strings['Display the first row as a header.']}</label>
                    &emsp;
                    <input type="checkbox" id="${id}-handsontable-col-header" name="handsontable-col-header" />
                    <label for="${id}-handsontable-col-header"> ${this.strings['Display the first column as a header.']}</label>
                  </div>
                </div>
              </div>
              <div class="field" style="display: none;">
                  <label for="${id}-handsontable-col-caption">${this.strings['Table caption']}</label>
                  <div class="field-content">
                    <div class="input">
                    <input type="text" id="${id}-handsontable-col-caption" name="handsontable-col-caption" />
                  </div>
                  <p class="help">
                    ${this.strings['A heading that identifies the overall topic of the table, and is useful for screen reader users'] /* eslint-disable-line max-len */}
                  </p>
                </div>
              </div>
              <br/>
              <div id="${id}-handsontable-container"></div>
              <input type="hidden" name="${name}" id="${id}" placeholder="${this.strings['Table']}">
            `;
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