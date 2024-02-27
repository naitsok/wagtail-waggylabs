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
                action: togglePreviewAll,
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
        } else if (toolbarButtons[i] === "fullscreen") {
            toolbar.push({
                name: "fullscreen",
                action: toggleFullScreen,
                className: "fa fa-arrows-alt",
                noDisable: true,
                noMobile: true,
                title: "Toggle Fullscreen",
                default: true,
            });
            shortcuts[toolbarButtons[i]] = "F11";
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
        action: (editor) => CodeMirror.showHint(
            editor.codemirror,
            getHinter(),
            {completeSingle: false}
        ),
    });
    shortcuts["autocomplete"] = "Cmd-Space";
    return [toolbar, shortcuts];
}

/**
 * Collects the citation labels into a list
 * @returns  - array of strings with citation labels
 */
function collectCites() {
    let cites = [];
    document.querySelectorAll('.waggylabs-label-cite').forEach((el) => {
        const input = el.getElementsByTagName('input')[0];
        if (input.value) { cites.push(input.value); }
    });
    return cites;
}

/**
 * Collects the equation reference labels 
 * @returns - list of strings with equation reference labels
 */
function collectEqRefs() {
    const eqRefs = [];
    // Equation reference from the equation blocks
    document.querySelectorAll('.waggylabs-label-equation').forEach((el) => {
        const input = el.getElementsByTagName('input')[0];
        if (input.value) { eqRefs.push(input.value); }
    });
    // Equation references from EasyMDEs
    const re = new RegExp(/\\label\{(.+?)\}/gi);
    const textAreas = document.getElementsByTagName("textarea");
    for (let i in textAreas) {
        if(textAreas[i].easyMDE) {
            while ((match = re.exec(textAreas[i].easyMDE.value())) !== null) {
                eqRefs.push(match[1]);
            }
        }
    }

    return eqRefs;
}

/**
 * Collects all the reference labels 
 * @returns - list of strings with reference labels
 */
function collectRefs() {
    const refs = collectEqRefs();
    // collect figures, listings, embeds, tables
    const refTypes = ['figure', 'table', 'listing', 'embed', 'blockquote'];
    refTypes.forEach((refType) => {
        document.querySelectorAll('.waggylabs-label-' + refType).forEach((el) => {
            const input = el.getElementsByTagName('input')[0];
            if (input.value) { refs.push(input.value); }
        });
    });
    return refs;
}

/**
 * Create hinter function for CodeMirror autocomplete addon
 * @returns - function that is invoked when autocomplete event is triggered, this 
 * function then provides the list of commands to complete. Commands are mainly LaTeX/
 * MathJax commands used in math and text environments.
 */
function getHinter() {
    const mathJaxTextCommands = getMathJaxTextCommands();
    const mathJaxMathCommands = getMathJaxMathCommands();
    const mathJaxEnvs = getMathJaxEnvs();
    const emojis = getEmojis(true);
    const citeRegex = new RegExp(/\\cite\{([^\}]*)$/i);
    const eqRefRegex = new RegExp(/\\eqref\{([^\}]*)$/i);
    const refRegex = new RegExp(/\\ref\{([^\}]*)$/i);
    const beginRegex = new RegExp(/\\begin\{([^\}]*)$/i);
    const endRegex = new RegExp(/\\end\{([^\}]*)$/i);
    const commandRegex = new RegExp(/\\[\w]*$/i);
    // const emojiRegex = new RegExp(/\:[\w\'\(\)\_\.]*$/i);
    const emojiRegex1 = new RegExp(/:$/i);
    const emojiRegex2 = new RegExp(/:([\w\_\(\)\'\.\!]+?):$/i);

    return function hintFunction(cm) {
        cm.noCompletion = true;

        const cur = cm.getCursor();
        
        const lineTillCursor = cm.getRange({line: cur.line, ch: 0}, cur);
        const allTillCursor = cm.getRange({line: 0, ch: 0}, cur);

        const inCiteMatch = citeRegex.exec(lineTillCursor);
        if (inCiteMatch) {
            const match = inCiteMatch[1].split(',').slice(-1)[0];
            let cites = collectCites();
            if (match) {
                const re = new RegExp('^' + match, 'i');
                cites = cites.filter((s) => { return re.test(s); });
            }
            cm.noCompletion = cites.length === 0;
            return {
                from: { line: cur.line, ch: cur.ch - (match ? match.length : 0), },
                to: { line: cur.line, ch: cur.ch, },
                list: cites.sort(),
            };
        }

        const eqRefMatch = eqRefRegex.exec(lineTillCursor);
        if (eqRefMatch) {
            const match = eqRefMatch[1];
            let eqRefs = collectEqRefs();
            if (match) {
                const re = new RegExp('^' + match, 'i');
                eqRefs = eqRefs.filter((s) => { return re.test(s); });
            }
            cm.noCompletion = eqRefs.length === 0;
            return {
                from: { line: cur.line, ch: cur.ch - (match ? match.length : 0), },
                to: { line: cur.line, ch: cur.ch, },
                list: eqRefs.sort(),
            };
        }

        const refMatch = refRegex.exec(lineTillCursor);
        if (refMatch) {
            const match = refMatch[1];
            let refs = collectRefs();
            if (match) {
                const re = new RegExp('^' + match, 'i');
                refs = refs.filter((s) => { return re.test(s); });
            }
            cm.noCompletion = refs.length === 0;
            return {
                from: { line: cur.line, ch: cur.ch - (match ? match.length : 0), },
                to: { line: cur.line, ch: cur.ch, },
                list: refs.sort(),
            };
        }

        const envMatch = beginRegex.exec(lineTillCursor) || endRegex.exec(lineTillCursor);
        if (envMatch) {
            const match = envMatch[1];
            if (match) {
                const re = new RegExp('^' + match, 'i');
                const mathJaxEnvCompletion = mathJaxEnvs.filter((s) => { return re.test(s); });
                cm.noCompletion = mathJaxEnvCompletion.length === 0;
                return {
                    from: { line: cur.line, ch: cur.ch - match.length, },
                    to: { line: cur.line, ch: cur.ch, },
                    list: mathJaxEnvCompletion,
                };
            }
            cm.noCompletion = false;
            return {
                from: { line: cur.line, ch: cur.ch, },
                to: { line: cur.line, ch: cur.ch, },
                list: mathJaxEnvs,
            };
        }

        const emojiMatch = emojiRegex1.exec(lineTillCursor);
        const skipEmojiMatch = emojiRegex2.exec(lineTillCursor);
        if (emojiMatch && !skipEmojiMatch) {
            emojiMatch[0] = emojiMatch[0].replace(/\(/g, '\\(').replace(/\)/g, '\\)').replace(/\./g, '\\.');
            const re = new RegExp('^' + emojiMatch[0], 'i');
            return {
                from: { line: cur.line, ch: cur.ch - emojiMatch[0].length, },
                to: { line: cur.line, ch: cur.ch, },
                list: emojis.filter((em) => { return re.test(em.text); }), 
            }
        }

        const commandMatch = commandRegex.exec(lineTillCursor);
        const inMath = ((allTillCursor.match(/\\begin\{[a-zA-Z\*]+\}/g) || []).length > (allTillCursor.match(/\\end\{[a-zA-Z\*]+\}/g) || []).length) ||
            ((allTillCursor.match(/^\\*\$|[^\\]\$/g) || []).length % 2 > 0) || ((allTillCursor.match(/^\\*\$\$|[^\\]\$\$/g) || []).length % 2 > 0);
        let commands = inMath ? mathJaxMathCommands : mathJaxTextCommands;
        if (commandMatch) {
            const re = new RegExp('^\\' + commandMatch[0], 'i');
            cm.noCompletion = inMath;
            return {
                from: { line: cur.line, ch: cur.ch - commandMatch[0].length, },
                to: { line: cur.line, ch: cur.ch, },
                list: commands.filter((s) => { return re.test(s); }),
            };
        }
        
        // return { list: [] };
        // return {
        //     from: { line: cur.line, ch: cur.ch, },
        //     to: { line: cur.line, ch: cur.ch, },
        //     list: commands,
        // };
    }
}

function getEndCompletion() {
    const beginRegex = new RegExp(/\\begin\{([^\}]+)$/i);
    const textCommandsRegex = new RegExp(/\\begin$|\\end$|\\cite$|\\eqref$|\\ref$/i);
    const labelCommandsRegex = new RegExp(/\\end\{[^\}]+$|\\cite\{[^\}]+$|\\eqref\{[^\}]+$|\\ref\{[^\}]+$/i);
    const closeBracketRegex = new RegExp(/^.*\}/i);
    // const emojiRegex = new RegExp(/:([\w\_\(\)\'\.\!]+?):$/i);

    return function endCompetionFunction(cm) {
        const cur = cm.getCursor();
        const lineTillCursor = cm.getRange({line: cur.line, ch: 0}, cur);
        const lineAfterCursor = cm.getLine(cur.line).slice(cur.ch);

        const beginMatch = beginRegex.exec(lineTillCursor);
        if (beginMatch) {
            cm.replaceRange('}\n\n\\end{' + beginMatch[1] + '}\n', cur);
            cm.setCursor({line: cur.line + 1, ch: 0});
            return false;
        }

        const textCommandsMatch = textCommandsRegex.exec(lineTillCursor);
        if (textCommandsMatch && (cm.getRange(cur, {line: cur.line, ch: cur.ch + 1}) !== "{")) {
            cm.replaceRange('{', cur);
            return true;
        }

        const labelCommandsMatch = labelCommandsRegex.exec(lineTillCursor);
        const closeBracketMatch = closeBracketRegex.exec(lineAfterCursor);
        if (labelCommandsMatch && !closeBracketMatch) {
            cm.replaceRange('}', cur);
            return false;
        }
        
        return false;
    }
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
 * Toggles side-by-side mode with correct handling of other EasyMDEs
 * on the page to correctly render MathJax equations.
 * @param {EaseMDE} editor - EasyMDE object
 */
function toggleSideBySide(editor) {
    // We need to keep other editors in preview mode
    // in order to correctly render MathJax refs in the
    // side by side mode
    if (!editor.isSideBySideActive()) {
        // Collects all the EasyMDE (except this one in side-by-side mode) data in order
        // to re-render markdown content and re-typeset MathJax
        // Needed to speed up typesetting and do not care about other content and EasyMDEs
        // on the page
        var wrapper = editor.codemirror.getWrapperElement();
        window.allMarkdown = '';
        var textAreas = document.getElementsByTagName("textarea");
        for (let i in textAreas) {
            if(textAreas[i].easyMDE && textAreas[i].easyMDE.element.id !== editor.element.id) {
                // now check if the EasyMDE contain equation, i.e. it is in only in the TeX mode
                window.allMarkdown = window.allMarkdown + updateTextIfEquation(textAreas[i].easyMDE.value(), textAreas[i].easyMDE);
            }
        }

        var allMarkdownElem = wrapper.querySelector('.waggylabs-all-markdown');
        if (!allMarkdownElem) {
            allMarkdownElem = document.createElement('div');
            allMarkdownElem.classList.add('waggylabs-all-markdown');
            allMarkdownElem.style.display = 'none';
            wrapper.insertBefore(allMarkdownElem, wrapper.lastChild);
        }
        allMarkdownElem.innerHTML = editor.options.previewRender(window.allMarkdown, editor);
        // store the necesarry values for the interval check and update of markdown and MathJax
        window.allMarkdownElem = allMarkdownElem;
        window.easyMDE = editor;
        window.mathJaxTimer = setInterval(resetMathJax, 1000);
    } else {
        clearInterval(window.mathJaxTimer);
    }
    // Actually go to side-by-side mode
    EasyMDE.toggleSideBySide(editor);
}

function toggleFullScreen(editor) {
    if (window.mathJaxTimer) {
        clearInterval(window.mathJaxTimer);
    }
    EasyMDE.toggleFullScreen(editor);
}

/**
 * Toggles preview mode for the specified editor
 * @param {EasyMDE} editor - EasyMDE editor object
 * @param {boolean} isPreview - the preview mode to set for the editor
 */
function togglePreview(editor, isPreview) {
    var cm = editor.codemirror;
    var wrapper = cm.getWrapperElement();
    var toolbar_div = editor.toolbar_div;
    var toolbar = editor.options.toolbar ? editor.toolbarElements.preview : false;
    var preview = wrapper.lastChild;

    // Turn off side by side if needed
    var sidebyside = cm.getWrapperElement().nextSibling;
    if (sidebyside.classList.contains('editor-preview-active-side'))
        EasyMDE.toggleSideBySide(editor);

    if (!preview || !preview.classList.contains('editor-preview-full')) {

        preview = document.createElement('div');
        preview.className = 'editor-preview-full';

        if (editor.options.previewClass) {

            if (Array.isArray(editor.options.previewClass)) {
                for (var i = 0; i < editor.options.previewClass.length; i++) {
                    preview.classList.add(editor.options.previewClass[i]);
                }

            } else if (typeof editor.options.previewClass === 'string') {
                preview.classList.add(editor.options.previewClass);
            }
        }

        wrapper.appendChild(preview);
    }

    var editorPreviewMode = preview.classList.contains('editor-preview-active');

    if (editorPreviewMode !== isPreview) {
        // Editor is not in the same preview state as others, 
        // preview mode must be changed
        if (editorPreviewMode) {
            preview.classList.remove('editor-preview-active');
            if (toolbar) {
                toolbar.classList.remove('active');
                toolbar_div.classList.remove('disabled-for-preview');
            }
        } else {
            // When the preview button is clicked for the first time,
            // give some time for the transition from editor.css to fire and the view to slide from right to left,
            // instead of just appearing.
            setTimeout(() => {
                preview.classList.add('editor-preview-active');
            }, 1);
            if (toolbar) {
                toolbar.classList.add('active');
                toolbar_div.classList.add('disabled-for-preview');
            }
        }
    }

    var preview_result = editor.options.previewRender(editor.value(), preview);
    if (preview_result !== null) {
        preview.innerHTML = preview_result;
    }
}

/**
 * Toggles the preview mode of all the EasyMDE editors
 * on the page depending on the preview mode of this 
 * editor (editor that toggled preview mode)
 * @param {EasyMDE} editor -  EasyMDE editor object
 * @param {boolean} isPreview - if present, forces the specified preview mode
 * @param {boolean} skipMathJax - when going into side-by-side mode MathJax
 * typeset is not needed right after going into preview mode; it is needed
 * only after going into side-by-side mode.
 */
function togglePreviewAll(editor, isPreview, skipMathJax) {
    if (window.mathJaxTimer) {
        clearInterval(window.mathJaxTimer);
    }

    if (isPreview === undefined) {
        isPreview = !editor.isPreviewActive();
    }
    var textAreas = document.getElementsByTagName("textarea");
    for (let i in textAreas) {
        if(textAreas[i].easyMDE) {
            togglePreview(textAreas[i].easyMDE, isPreview);
        }
    }
    if (isPreview && skipMathJax === undefined) {
        // var preview = editor.codemirror.getWrapperElement().lastChild;
        MathJax.typesetClear();
        MathJax.texReset();
        MathJax.typeset([document.getElementById("main")]);
    }
}

/**
 * Resets MathJax to correctly display equation numbers during side-by-side editing
 * @param {EasyMDE} editor - EasyMDE object
 */
function resetMathJax() {
    if (window.allMarkdown && window.allMarkdownElem && window.easyMDE) {
        window.allMarkdownElem.innerHTML = renderMarkdown(window.allMarkdown, window.easyMDE);
        MathJax.typesetClear();
        MathJax.texReset();
        MathJax.typeset([window.allMarkdownElem, window.easyMDE.gui.sideBySide]);
    }
    
}

function easymdeAttach(id) {
    var textArea = document.getElementById(id);
    var toolbar = undefined;
    var shortcuts = undefined;
    if (textArea.getAttribute("easymde-toolbar")) {
        [toolbar, shortcuts] = createToolbar(textArea.getAttribute("easymde-toolbar"));
    } 

    var mde = new EasyMDE({
        element: textArea,
        autofocus: false,
        autoDownloadFontAwesome: true, // autoDownloadFontAwesome,
        lineNumbers: true,
        minHeight: textArea.getAttribute("easymde-min-height") || undefined,
        maxHeight: textArea.getAttribute("easymde-max-height") || undefined,
        overlayMode: {
            mode: CodeMirror.getMode({}, "stex"),
            combine: textArea.getAttribute("easymde-combine").toLowerCase() === "true",
        },
        renderingConfig: {
            codeSyntaxHighlighting: true,
        },
        spellChecker: false,
        showIcons: (textArea.getAttribute("easymde-toolbar")) ? undefined : ["strikethrough", "code", "table"],
        toolbar: (textArea.getAttribute("easymde-toolbar")) ? toolbar : undefined,
        shortcuts: (textArea.getAttribute("easymde-toolbar")) ? shortcuts : undefined,
        status: createStatusBar(textArea.getAttribute("easymde-status")),
        unorderedListStyle: "-",
    });
    
    mde.options.previewRender = (plainText, preview) => {
        // if (mde.isSideBySideActive()) {
        //     setTimeout(() => {
        //         resetMathJax(mde);
        //     }, 1000);
        // }
        return renderMarkdown(plainText, mde);
    };
    mde.render();

    // Save the codemirror instance on the original html element for later use.
    mde.element.codemirror = mde.codemirror;

    mde.codemirror.on("change", () => {
        document.getElementById(id).value = mde.value();
    });

    mde.codemirror.on("keyup", (cm, event) => {
        const ignoreKeys = ["Meta", "Alt", "Control", "F1", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "ArrowUp", "ArrowLeft", "ArrowRight", "ArrowDown", "ContextMenu", " ", "Enter", "Shift", "CapsLock", "Tab", "Delete", "Home", "PrintScreen", "PageUp", "PageDown", "NumLock", "Insert", "Backspace", "Escape", undefined];
        if (!ignoreKeys.includes(event.key)) {
            CodeMirror.showHint(mde.codemirror, getHinter(), {completeSingle: false});
        }
    });
    // const completionFunction = getEndCompletion();
    mde.codemirror.on("endCompletion", () => {
        if (!mde.codemirror.noCompletion) {
            if (getEndCompletion()(mde.codemirror)) {
                // let event = document.createEvent()
                // document.getElementById(id).dispatchEvent(new KeyboardEvent('keypress',{'key':'Ctrl+Space'}));
                CodeMirror.showHint(mde.codemirror, getHinter(), {completeSingle: false});
            }
        }
    })

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
function refreshCodeMirror(e) {
    setTimeout(() => {
            e.CodeMirror.refresh();
            e.CodeMirror.focus();
        }, 200
    );
}

// Wagtail < 3.0
document.addEventListener('shown.bs.tab', () => {
    document.querySelectorAll('.CodeMirror').forEach((e) => {
        refreshCodeMirror(e);
    });
});

// Wagtail >= 3.0
document.addEventListener('wagtail:tab-changed', () => {
    document.querySelectorAll('.CodeMirror').forEach((e) => {
        refreshCodeMirror(e);
    });
});