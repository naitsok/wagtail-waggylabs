/**
 * Telepath adapter for the code block
 */
(() => {
    class CodeBlockDefinition extends window.wagtailStreamField.blocks.StructBlockDefinition {
        render(placeholder, prefix, initialState, initialError) {
            const block = super.render(
                placeholder,
                prefix,
                initialState,
                initialError,
            );

            const modeField = document.getElementById(prefix + "-mode");
            const codeField = document.getElementById(prefix + "-code");
            var cm = CodeMirror.fromTextArea(codeField, {
                value: codeField.value,
                mode: modeField.value,
                lineNumbers: true,
                styleActiveLine: true,
                matchBrackets: true,
            });
            cm.on("change", function() {
                cm.save();
            });
            const updateCodeMirrorMode = () => {
                cm.setOption("mode", modeField.value);
            };
            updateCodeMirrorMode();
            modeField.addEventListener("change", updateCodeMirrorMode);

            return block;
        }
    }
    window.telepath.register('waggylabs.blocks.CodeBlock', CodeBlockDefinition);
})();