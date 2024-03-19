/*
 * vim:sw=4 ts=4 et:
 * Copyright (c) 2015-present Torchbox Ltd.
 * hello@torchbox.com
 *
 * Permission is granted to anyone to use this software for any purpose,
 * including commercial applications, and to alter it and redistribute it
 * freely. This software is provided 'as-is', without any express or implied
 * warranty.
 * 
 * Updated by Konstantin Tamarov for Waggy Labs to typeset MathJax.
 */

/*
 * Used to initialize Easy MDE when Markdown blocks are used in StreamFields
 */

/**
 * Gets Font Awesome icon for EasyMDE math buttons
 * @param {string} pattern - math pattern
 * @returns CSS class for the Font Awesome icon, free version has only subscript and superscript icons
 */
function getMenuItemIcon(pattern) {
    switch (pattern) {
        case "subscript": return "fa fa-subscript";
        case "superscript": return "fa fa-superscript";
        default: return undefined;
    }
}

/**
 * Gets text value for EasyMDE math button when no Icon available
 * @param {string} pattern - math pattern
 * @returns Text for button because there are no suitable Font Awesome Icons
 */
function getMenuItemText(pattern) {
    switch (pattern) {
        case "equation": return "{Eq}";
        case "matrix": return "[M]";
        case "align": return "{Al}";
        case "split": return "{Sp}";
        case "multiline": return "{Mu}";
        case "gather": return "{Ga}";
        case "alignat": return "{At}";
        case "flalign": return "{Fl}";
        default: return undefined;
    }
}

/**
 * @param {string} toolbarConfig - the configuration string with toolbar buttons, such as
 *  "bold,italic,strikethrough,|,unordered-list,ordered-list,link,|,preview,side-by-side,fullscreen,guide"
 * @returns toolbar and shortcuts for EasyMDE
 */
function createToolbar(toolbarConfig) {
    if (toolbarConfig === 'false') {
        return false;
    }
    // Math patterns from the AMS Math LaTeX package
    var allMathPatterns = ["subscript", "superscript", "equation", "matrix", "split", "multiline", "gather", "align", "alignat", "flalign"];
    // Shortcuts for the math patterns
    var allShortcuts = {
        "subscript": "Cmd--",
        "superscript": "Cmd-=",
        "equation": "Cmd-Alt-E",
        "matrix": "Cmd-Alt-M",
        "split": "Cmd-Alt-S",
        "multiline": "Cmd-Alt-U",
        "gather": "Cmd-Alt-G",
        "align": "Cmd-Alt-A",
        "alignat": "Cmd-Alt-T",
        "flalign": "Cmd-Alt-F"
    }
    
    // create math button function
    const createMathButton = (pattern) => {
        return {
            name: pattern.toLowerCase(),
            action: (editor) => {
                var doc = editor.element.codemirror.getDoc();
                var startCursor = doc.getCursor("from");
                var endCursor = doc.getCursor("to");
                var selection = doc.getSelection();
                var data = "";

                if (pattern === "superscript" || pattern === "subscript") {
                    if (selection.length !== 0) {
                        data = "\\text{" + selection + "}"; 
                    }
                    data = (pattern === "subscript") ? "$"+ data + "_{}$" : "$"+ data + "^{}$";
                    doc.replaceRange(data, startCursor, endCursor);
                    doc.setCursor(startCursor.line, startCursor.ch + data.length - 2);
                }
                else {
                    var addLine = 0;
                    if (selection.length === 0) {
                        data = "\\begin{" + pattern + "}\n\n\\end{" + pattern + "}\n";
                    }
                    else {
                        data = "\\begin{" + pattern + "}\n" + selection + "\n\\end{" + pattern + "}\n";
                    }
                    // check if the beginning of selection is at the beginning of line or not
                    if (startCursor.ch !== 0) {
                        data = "\n" + data;
                        addLine = 1;
                    }
                    doc.replaceRange(data, startCursor, endCursor);
                    // Put the cursor at the new position withing the \begin{...} block
                    var selectedLines = selection.split("\n");
                    doc.setCursor({
                        line: startCursor.line + addLine + selectedLines.length,
                        ch: selectedLines[selectedLines.length - 1].length
                    });
                }
                editor.element.codemirror.focus();
            },
            className: getMenuItemIcon(pattern),
            text: getMenuItemText(pattern),
            title: pattern.charAt(0).toUpperCase() + pattern.slice(1)
        }
    }

    // First prepare menu if there is "equation", "matrix", "align", etc. present in the toolbar settings
    var toolbar = [];
    var shortcuts = {};
    var toolbarButtons = toolbarConfig.split(",");
    for (let i = 0; i < toolbarButtons.length; i++) {
        if (allMathPatterns.indexOf(toolbarButtons[i]) >= 0) {
            toolbar.push(createMathButton(toolbarButtons[i]));
            shortcuts[toolbarButtons[i]] = allShortcuts[toolbarButtons[i]];
        } else if (toolbarButtons[i] === "preview") {
            toolbar.push({
                name: "preview",
                action: togglePreview,
                className: "fa fa-eye",
                noDisable: true,
                title: "Toggle Preview",
                default: true,
            });
            shortcuts[toolbarButtons[i]] = "Cmd-P";
        } else if (toolbarButtons[i] === "side-by-side") {
            toolbar.push({
                name: "side-by-side",
                action: toggleSideBySide,
                className: "fa fa-columns",
                noDisable: true,
                noMobile: true,
                title: "Toggle Side by Side",
                default: true,
            });
            shortcuts[toolbarButtons[i]] = "F9";
        } else {
            toolbar.push(toolbarButtons[i]);
        }
    }
    // Finally add autocomplete hidden button
    toolbar.push({
        name: "autocomplete",
        className: "d-none",
        noDisable: true,
        noMobile: true,
        title: "Autocomplete",
        default: true,
        action: (editor) => CodeMirror.showHint(cm, getHinter(),
            { 
                completeSingle: false,
                closeCharacters: RegExp(/[\s()\[\]{};:>]/),
            }),
    });
    shortcuts["autocomplete"] = "Cmd-Space";
    return [toolbar, shortcuts];
}

/**
 * @param {string} statusConfig - true for default status bar, fals for no bar,
 * list of comma separated values for custom toolbar
 * @returns - configuration of the status bar
 */
function createStatusBar(statusConfig) {
    if (statusConfig === "false") {
        return false;
    }
    if (statusConfig === "true") {
        return ['autosave', 'lines', 'words', 'cursor'];
    }
    return statusConfig.split(",");
}

/**
 * Updates the text value of the EasyMDE if it is used for equation blocks. Updating
 * is needed to add \begin{equation} and \label{...} commands if they are absent.
 * @param {*} text - value of EasyMDE, i.e. EasyMDE.value()
 * @param {*} mde - instance of EasyMDE Editor
 * @returns - updated text with necessary commands
 */
function updateTextIfEquation(text, mde) {
    // Check if the editor is in LaTeX or not, it means that we are in the Equation block.
    // Then \begin{equation} and \label{...} needs to be added if they are absent
    if (mde && mde.options && mde.options.overlayMode && !mde.options.overlayMode.combine) {
        text = text.trim().replace(/^\$+|\$+$/, '');
        // add \begin{equation}, \end{equation} if not present
        if (text.search(/\\begin\{/i) === -1) {
            text = "\\begin{equation}\n" + text + "\\end{equation}";
        }
        if (text.search(/\\label\{/i) === -1) {
            // label not found, we have to add it from the neighbour Label block
            const label = mde.element.closest(".struct-block").getElementsByTagName("input")[0];
            if (label.value) {
                const idx = text.search(/\\end\{/i);
                text = text.slice(0, idx) + "\\label{" + label.value + "}\n" + text.slice(idx);
            }
        }
    }

    return text;
}

/**
 * Collects all the typed markdown text from all the EasyMDE except the
 * specified one. The collected text is then typeset with markdown and mathjax
 * to correctly generate the equation references. The function is used to
 * correctly toggle the preview of the specified editor with generated equation\
 * references.
 * @param {easyMDE} editor - EasyMDE object 
 */
function collectTypesetMarkdown(editor) {
    // Collects all the EasyMDE (except this one in side-by-side mode) data in order
    // to re-render markdown content and re-typeset MathJax
    // Needed to speed up typesetting and do not care about other content and EasyMDEs
    // on the page
    var wrapper = editor.codemirror.getWrapperElement();
    var allMarkdown = '';
    var textAreas = document.getElementsByTagName("textarea");
    for (let i in textAreas) {
        if(textAreas[i].easyMDE && textAreas[i].easyMDE.element.id !== editor.element.id) {
            // now check if the EasyMDE contain equation, i.e. it is in only in the TeX mode
            allMarkdown = allMarkdown + updateTextIfEquation(textAreas[i].easyMDE.value(), textAreas[i].easyMDE);
        }
    }

    var allMarkdownElem = document.getElementById("waggylabs-all-markdown");
    if (!allMarkdownElem) {
        allMarkdownElem = document.createElement("div");
        allMarkdownElem.setAttribute("id", "waggylabs-all-markdown");
        allMarkdownElem.style.display = "none";
        wrapper.insertBefore(allMarkdownElem, wrapper.lastChild);
    }
    allMarkdownElem.innerHTML = renderMarkdown(allMarkdown, editor);
}

/**
 * Resets MathJax to correctly display equation numbers during side-by-side editing
 * @param {DOM element} previewElem - EasyMDE preview DOM element in which Mathjax is typeset.
 */
function resetMathJax(previewElem) {
    var allMarkdownElem = document.getElementById("waggylabs-all-markdown");
    if (allMarkdownElem) {
        MathJax.typesetClear();
        MathJax.texReset();
        MathJax.typeset([allMarkdownElem, previewElem]);
    }
}

function togglePreview(editor) {
    if (window.mathJaxTimer) {
        clearInterval(window.mathJaxTimer);
    }

    if (editor.isSideBySideActive()) {
        EasyMDE.toggleSideBySide(editor);
    }

    EasyMDE.togglePreview(editor);

    if (!editor.isPreviewActive()) {
        var previewElem = editor.codemirror.getWrapperElement().lastChild;
        collectTypesetMarkdown(editor);
        resetMathJax(previewElem);
    }
}

function toggleSideBySide(editor) {
    if (!editor.isSideBySideActive()) {
        collectTypesetMarkdown(editor);
        window.mathJaxTimer = setInterval(() => { 
            collectTypesetMarkdown(editor);
            resetMathJax(editor.gui.sideBySide); 
        }, 1000);
    } else {
        clearInterval(window.mathJaxTimer);
    }
    // Actually go to side-by-side mode
    EasyMDE.toggleSideBySide(editor);
}

function easymdeAttach(id, autodownload, minHeight, maxHeight, stexCombine, toolbar, statusbar) {
    var textArea = document.getElementById(id);
    shortcuts = undefined;
    if (toolbar) {
        [toolbar, shortcuts] = createToolbar(toolbar);
    } 

    var mde = new EasyMDE({
        element: textArea,
        autofocus: false,
        autoDownloadFontAwesome: autodownload, // autoDownloadFontAwesome,
        lineNumbers: true,
        minHeight: minHeight,
        maxHeight: maxHeight,
        overlayMode: {
            mode: CodeMirror.getMode({}, "stex"),
            combine: stexCombine,
        },
        renderingConfig: {
            codeSyntaxHighlighting: true,
        },
        spellChecker: false,
        showIcons: toolbar ? undefined : ["strikethrough", "code", "table"],
        toolbar: toolbar ? toolbar : undefined,
        shortcuts: toolbar ? shortcuts : undefined,
        status: statusbar,
        unorderedListStyle: "-",
    });
    
    mde.options.previewRender = (plainText, preview) => {
        return renderMarkdown(plainText, mde);
    };
    mde.render();

    // Save the codemirror instance on the original html element for later use.
    mde.element.codemirror = mde.codemirror;
    mde.codemirror.hintState = HintState.CLOSED;

    mde.codemirror.on("change", () => {
        document.getElementById(id).value = mde.value();
    });

    mde.codemirror.on("keyup", (cm, event) => {
        const ignoreKeys = ["Meta", "Alt", "Control", "F1", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "ArrowUp", "ArrowLeft", "ArrowRight", "ArrowDown", "ContextMenu", " ", "Enter", "Shift", "CapsLock", "Tab", "Delete", "Home", "PrintScreen", "PageUp", "PageDown", "NumLock", "Insert", "Escape", undefined]; //"Backspace", 
        if (!ignoreKeys.includes(event.key)) {
            if (mde.codemirror.hintState === HintState.CLOSED) {
                CodeMirror.showHint(cm, getHinter(),
                    { 
                        completeSingle: false,
                        closeCharacters: RegExp(/[\s()\[\]{};:>]/),
                    });
            }
        }
    });
    // const completionFunction = getEndCompletion();
    mde.codemirror.on("endCompletion", () => {
        getEndCompletion()(mde.codemirror);
    });

    // Attach the mde object to the text area.
    // It is needed for the new togglePreview function,
    // which toggles preview of all the EasyMDEs on the page.
    // It is in turn needed for correct rendering of MathJax
    // equation references.
    textArea.easyMDE = mde;
}

/*
* Used to initialize content when MarkdownFields are used in admin panels.
*/
/*
function refreshCodeMirror(e) {
    setTimeout(() => {
            e.CodeMirror.refresh();
            e.CodeMirror.focus();
        }, 200
    );
}
*/

document.addEventListener('wagtail:tab-changed', () => {
    document.querySelectorAll('.CodeMirror').forEach(function(e) {
        setTimeout(
            function() {
                e.CodeMirror.refresh();
            }, 100
        );
    });
});