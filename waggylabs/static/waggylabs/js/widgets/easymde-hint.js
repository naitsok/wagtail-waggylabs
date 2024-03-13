/*
 * Copyright (c) 2024-present Konstantin Tamarov
 * contact@ktamarov.com
 *
 * Permission is granted to anyone to use this software for any purpose,
 * including commercial applications, and to alter it and redistribute it
 * freely. This software is provided 'as-is', without any express or implied
 * warranty.
 * 
 */

/*
* Autocomplete feature for EasyMDE Markdown editor to show hints for LaTeX
* equations and emojis. Developed using the show-hint.js addon for CodeMirror 5.
* 
* Requires markdown-mathjax.js and markdown-emoji.js.
*/

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
 * HintState class has states to transfer between hint fincution and 
 * endComppletion function
 */
const HintState = Object.freeze({
    CLOSED: "Closed", // hint does not display completing options
    LAUNCHED: "Launched", // hint function was called
    TEXT: "Text", // hint list is open during typing normal text
    MATH: "Math", // hint list is open in math LaTeX environment
    BEGIN_ENV: "BeginEnv", // hint is open inside \begin{...}
    END_ENV: "EndEnv", // hint is open inside \end{...}
    CITE: "Cite", // hint is open inside \cite{...}
    EQREF: "Eqref", // hint is open inside \eqref{...}
    REF: "Ref", // hint is open inside \ref{...}
    EMOJI: "Emoji", // hint is open for emojis
    EMPTY: "Empty", // hint function returns empty list
    HINT: "Hint", // To show hint again (call hint function)
});

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
        // define the state of codemirror autocomplete
        if (!cm.hintState) {
            cm.hintState = HintState.CLOSED;
        }
        cm.hintState = HintState.LAUNCHED;

        // cm.noCompletion = true;

        const cur = cm.getCursor();
        
        const lineTillCursor = cm.getRange({line: cur.line, ch: 0}, cur);
        const allTillCursor = cm.getRange({line: 0, ch: 0}, cur);

        const inCiteMatch = citeRegex.exec(lineTillCursor);
        if (inCiteMatch) {
            cm.hintState = HintState.CITE;
            const match = inCiteMatch[1].split(',').slice(-1)[0];
            let cites = collectCites();
            if (match) {
                const re = new RegExp('^' + match, 'i');
                cites = cites.filter((s) => { return re.test(s); });
            }
            cm.hintState = (cites.length === 0) ? HintState.EMPTY : HintState.CITE;
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
            cm.hintState = (eqRefs.length === 0) ? HintState.EMPTY : HintState.EQREF;
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
            cm.hintState = (refs.length === 0) ? HintState.EMPTY : HintState.REF;
            return {
                from: { line: cur.line, ch: cur.ch - (match ? match.length : 0), },
                to: { line: cur.line, ch: cur.ch, },
                list: refs.sort(),
            };
        }

        const envMatch = beginRegex.exec(lineTillCursor) || endRegex.exec(lineTillCursor);
        if (envMatch) {
            const match = envMatch[1];
            cm.hintState = envMatch[0].includes("begin") ? HintState.BEGIN_ENV : HintState.END_ENV;
            if (match) {
                // We are inside to select environment, i.e. after the first { in \begin{ or \end{
                const re = new RegExp('^' + match, 'i');
                const mathJaxEnvCompletion = mathJaxEnvs.filter((s) => { return re.test(s); });
                cm.hintState = (mathJaxEnvCompletion.length === 0) ? HintState.EMPTY : cm.hintState;
                return {
                    from: { line: cur.line, ch: cur.ch - match.length, },
                    to: { line: cur.line, ch: cur.ch, },
                    list: mathJaxEnvCompletion,
                };
            }
            // here we are just after { in \begin{ or \end{
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
            const emojiCompletion = emojis.filter((em) => { return re.test(em.text); });
            cm.hintState = (emojiCompletion.length === 0) ? HintState.EMPTY : HintState.EMOJI;
            return {
                from: { line: cur.line, ch: cur.ch - emojiMatch[0].length, },
                to: { line: cur.line, ch: cur.ch, },
                list: emojiCompletion, 
            }
        }

        // Finally veryify if we are in normal text mode or we are inside the
        // LaTeX math environment and display the correct hints based on that
        const commandMatch = commandRegex.exec(lineTillCursor);
        const inMath = ((allTillCursor.match(/\\begin\{[a-zA-Z\*]+\}/g) || []).length > (allTillCursor.match(/\\end\{[a-zA-Z\*]+\}/g) || []).length) ||
            ((allTillCursor.match(/^\\*\$|[^\\]\$/g) || []).length % 2 > 0) || ((allTillCursor.match(/^\\*\$\$|[^\\]\$\$/g) || []).length % 2 > 0);
        let commands = inMath ? mathJaxMathCommands : mathJaxTextCommands;
        cm.hintState = inMath ? HintState.MATH : HintState.TEXT;
        if (commandMatch) {
            const re = new RegExp('^\\' + commandMatch[0], 'i');
            const commandsCompletion = commands.filter((s) => { return re.test(s); });
            cm.hintState = (commandsCompletion.length === 0) ? HintState.EMPTY : cm.hintState;
            return {
                from: { line: cur.line, ch: cur.ch - commandMatch[0].length, },
                to: { line: cur.line, ch: cur.ch, },
                list: commandsCompletion,
            };
        }

        // None of the completion matched
        cm.hintState = HintState.EMPTY;
    }
}

function getEndCompletion() {
    const beginRegex = new RegExp(/\\begin\{([^\}]+)$/i);
    const textCommandsRegex = new RegExp(/\\begin$|\\end$|\\cite$|\\eqref$|\\ref$/i);
    // const labelCommandsRegex = new RegExp(/\\end\{[^\}]+$|\\cite\{[^\}]+$|\\eqref\{[^\}]+$|\\ref\{[^\}]+$/i);
    const closeBracketRegex = new RegExp(/^.*\\.+\{[^\}]+$/i);
    // const emojiRegex = new RegExp(/:([\w\_\(\)\'\.\!]+?):$/i);

    return function endCompetionFunction(cm) {

        if ((cm.hintState === HintState.EMPTY) ||
            (cm.hintState === HintState.CLOSED)) {
            cm.hintState = HintState.CLOSED;
            return;
        }

        const cur = cm.getCursor();
        const lineTillCursor = cm.getRange({line: cur.line, ch: 0}, cur);
        const lineAfterCursor = cm.getLine(cur.line).slice(cur.ch);

        // const beginMatch = beginRegex.exec(lineTillCursor);
        // if (beginMatch) {
        if (cm.hintState === HintState.BEGIN_ENV) {
            const beginMatch = beginRegex.exec(lineTillCursor);
            if (beginMatch) {
                cm.replaceRange('}\n\n\\end{' + beginMatch[1] + '}\n', cur);
                cm.setCursor({line: cur.line + 1, ch: 0});
            }
            cm.hintState = HintState.CLOSED;
            return;
        }

        if ((cm.hintState === HintState.TEXT) && 
            textCommandsRegex.exec(lineTillCursor) &&
            (cm.getRange(cur, {line: cur.line, ch: cur.ch + 1}) !== "{")) {
            cm.replaceRange('{', cur);
            cm.hintState = HintState.CLOSED;
            // let event = document.createEvent();
            //cm.getWrapperElement().dispatchEvent(new KeyboardEvent('keydown', {'key': 'Cmd+Space'}));
            CodeMirror.showHint(cm, getHinter(),
                { 
                    completeSingle: false,
                    closeCharacters: RegExp(/[\s()\[\]{};:>]/),
                });
            return;
        }

        /* const textCommandsMatch = textCommandsRegex.exec(lineTillCursor);
        if (textCommandsMatch && (cm.getRange(cur, {line: cur.line, ch: cur.ch + 1}) !== "{")) {
            cm.replaceRange('{', cur);
            return true;
        } */

        if ((cm.hintState === HintState.CITE) ||
            (cm.hintState === HintState.END_ENV) ||
            (cm.hintState === HintState.EQREF) ||
            (cm.hintState === HintState.REF)) {
            const closeBracketMatch = closeBracketRegex.exec(lineTillCursor);
            if (closeBracketMatch) {
                cm.replaceRange('}', cur);
            }
            cm.hintState = HintState.CLOSED;
            return;
        }

        /* const labelCommandsMatch = labelCommandsRegex.exec(lineTillCursor);
        const closeBracketMatch = closeBracketRegex.exec(lineAfterCursor);
        if (labelCommandsMatch && !closeBracketMatch) {
            cm.replaceRange('}', cur);
            return false;
        } */

        cm.hintState = HintState.CLOSED;
    }
}