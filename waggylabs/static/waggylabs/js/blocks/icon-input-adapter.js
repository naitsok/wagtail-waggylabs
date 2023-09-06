/**
 * Telepath adapter for the incon input block.
*/
(() => {
    function IconInput(html, config) {
        this.html = html;
        this.baseConfig = config;
    }
    IconInput.prototype.render = function(placeholder, name, id, initialState) {
        placeholder.outerHTML = this.html.replace(/__NAME__/g, name).replace(/__ID__/g, id);

        var element = document.getElementById(id);
        element.value = initialState;
        autocompleteAttach(id);

        // define public API functions for the widget:
        // https://docs.wagtail.io/en/latest/reference/streamfield/widget_api.html
        return {
            idForLabel: null,
            getValue: () =>  {
                return element.value;
            },
            getState: () =>  {
                return element.value;
            },
            setState: () =>  {
                throw new Error('IconInput.setState is not implemented');
            },
            getTextLabel: (opts) => {
                if (!element.value) return '';
                var maxLength = opts && opts.maxLength,
                    result = element.value;
                if (maxLength && result.length > maxLength) {
                    return result.substring(0, maxLength - 1) + '…';
                }
                return result;
            },
            focus: () =>  {
                setTimeout(() =>  {
                    element.focus();
                }, 50);
            },
        };
    };

    window.telepath.register('waggylabs.widgets.IconInput', IconInput);
})();