/**
 * Telepath adapter for the Markdown textarea block.
*/
(() => {
    function MarkdownTextarea(html, config) {
        this.html = html;
        this.baseConfig = config;
    }
    MarkdownTextarea.prototype.render = function(placeholder, name, id, initialState) {
        placeholder.outerHTML = this.html.replace(/__NAME__/g, name).replace(/__ID__/g, id);

        var element = document.getElementById(id);
        element.value = initialState;

        easymdeAttach(id);

        // define public API functions for the widget:
        // https://docs.wagtail.io/en/latest/reference/streamfield/widget_api.html
        return {
            idForLabel: null,
            getValue: () => {
                return element.value;
            },
            getState: () => {
                return element.value;
            },
            setState: () => {
                throw new Error('MarkdownTextarea.setState is not implemented');
            },
            getTextLabel: (opts) =>  {
                if (!element.value) return '';
                var maxLength = opts && opts.maxLength,
                    result = element.value;
                if (maxLength && result.length > maxLength) {
                    return result.substring(0, maxLength - 1) + '…';
                }
                return result;
            },
            focus: () =>  {
                setTimeout(() => {
                    element.codemirror.focus();
                }, 50);
            },
        };
    };

    window.telepath.register('waggylabs.widgets.MarkdownTextarea', MarkdownTextarea);
})();