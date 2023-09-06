(function() {
    function MathTextarea(html, config) {
        this.html = html;
        this.baseConfig = config;
    }
    MathTextarea.prototype.render = function(placeholder, name, id, initialState) {
        placeholder.outerHTML = this.html.replace(/__NAME__/g, name).replace(/__ID__/g, id);

        var element = document.getElementById(id);
        element.value = initialState;

        const previewDiv = document.createElement("div");
        element.parentNode.insertBefore(previewDiv, element.nextSibling);
       
        var cm = CodeMirror.fromTextArea(element, {
            value: element.value,
            mode: element.getAttribute("codemirror-mode"),
            lineNumbers: true,
            styleActiveLine: true,
            matchBrackets: true
        });

        const updatePreviewDiv = () => {
            var cmValue = cm.getValue().toLowerCase();
            if (cmValue.length !== 0) {
                if (cmValue.startsWith("\\begin") || cmValue.startsWith("$$")) {
                    previewDiv.innerHTML = cm.getValue();
                }
                else {
                    previewDiv.innerHTML = "\\begin{equation}" + cm.getValue() + "\\end{equation}";
                }
            }
        }

        cm.on("change", function() {
            cm.save();
            updatePreviewDiv();

            MathJax.texReset();
            MathJax.typesetClear([previewDiv]);
            MathJax.typeset([previewDiv]);
        });

        updatePreviewDiv();


        // define public API functions for the widget:
        // https://docs.wagtail.io/en/latest/reference/streamfield/widget_api.html
        return {
            idForLabel: null,
            getValue: function() {
                return element.value;
            },
            getState: function() {
                return element.value;
            },
            setState: function() {
                throw new Error('MathTextarea.setState is not implemented');
            },
            getTextLabel: function(opts) {
                if (!element.value) return '';
                var maxLength = opts && opts.maxLength,
                    result = element.value;
                if (maxLength && result.length > maxLength) {
                    return result.substring(0, maxLength - 1) + '…';
                }
                return result;
            },
            focus: function() {
                setTimeout(function() {
                    cm.focus();
                }, 50);
            },
        };
    };

    window.telepath.register('waggylabs.widgets.MathTextarea', MathTextarea);
})();