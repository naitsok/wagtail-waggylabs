/**
 * Removes label elements from child page bodies. It happens when there are several
 * page bodies in page list on one page.
 * @param {DOM element} bodyElement - parent .waggylabs-page-body element
 * @param {DOM element} blockElements - selected .waggylabs-label-{type} element in
 * the parent .waggylabs-page-body element, contains unnecessary .waggylabs-label-{type} element
 * from child .waggylabs-page-body elements
 * @param {String} blockType - type of .waggylabs-label-{type} element, e.g. figure, listing, etc
 * @returns 
 */
function removePageBodyElements(bodyElement, blockElements, blockType) {
    blockElements = Array.from(blockElements);
    bodyElement.querySelectorAll('.waggylabs-page-body').forEach((childBodyElem) => {
        childBodyElem.querySelectorAll('.waggylabs-label-' + blockType).forEach((labelElem) => {
            blockElements = blockElements.filter((val) => { return val !== labelElem; });
        });
    });
    return blockElements;
}

/**
 * Processes figure, table, listing, blockquote references before 
 * MathJax does the same for equations.
 * @param {DOM element} element - element which innerHTML needs processing
 */
function prepareReferences(element) {
    const blockTypes = ['blockquote', 'embed', 'figure', 'listing', 'table'];
    blockTypes.forEach((blockType) => {
        let labelElements = element.querySelectorAll('.waggylabs-label-' + blockType);
        labelElements = removePageBodyElements(element, labelElements, blockType);
        labelElements.forEach((blockElem, i) => {
            const blockLabelElem = blockElem.querySelector('.waggylabs-entity-label');
            if (blockLabelElem) {
                blockLabelElem.innerHTML = blockLabelElem.innerHTML.trim() + ' ' + String(i + 1) + '.';
            }
        });
        // Two separate loops are needed because the loop below changes all the innerHTML and 
        // it conflicts with updating innerHTML of label element
        labelElements.forEach((blockElem, i) => {
            // Replace \ref{...} blocks with numbers of corresponding blocks
            const re = new RegExp('\\\\ref\{' + blockElem.id + '\}', 'g');
            element.innerHTML = element.innerHTML.replace(re, 
                `<span class="reference"><a href="#${blockElem.id}">${i + 1}</a></span>`);
        });
    });
}

/**
 * Processes literature citations and gererates references
 * @param {DOM element} element - element which innterHTML needs processing 
 */
function prepareCitations(element) {
    const labelIds = []; // needed to collect the ids of the elements containing citations
    let labelElements = element.querySelectorAll('.waggylabs-label-cite');
    labelElements = removePageBodyElements(element, labelElements, 'cite');
    labelElements.forEach((citeElem, idx) => {
        citeElem.innerHTML = idx + 1;
        labelIds.push(citeElem.id);
    });
    const re = /\\cite{(.*?)}/g;
    const matches = [];
    const citeHTMLs = [];
    let match;
    while (match = re.exec(element.innerHTML)) {
        let citeIds = [];
        // there can be more than one citation
        let cites = match[1].split(','); 
        // keeps the ids of for the current \cite{...}
        cites.forEach((cite) => {
            citeIds.push(labelIds.indexOf(cite));
        });

        citeIds.sort();
        let citeHTML = '';
        citeIds.forEach((citeId) => {
            if (citeId === -1) {
                citeHTML = citeHTML + `<span class="reference"><a href="#">???</a></span>,`;
            }
            else {
                citeHTML = citeHTML + `<span class="reference"><a href="#${labelIds[citeId]}">${citeId + 1}</a></span>,`;
            }
        });

        matches.push(match[0]);
        citeHTMLs.push('[' + citeHTML.slice(0, -1) + ']');
    }
    matches.forEach((match, idx) => {
        element.innerHTML = element.innerHTML.replace(match, citeHTMLs[idx]);
    });
}

/**
 * Adds scroll-margin-top to anchor links for correct navbar position
 * @param {DOM element} element - element within which scroll-margin-top is updated
 */
function prepareScrollMarginTop(element) {
    const navbar = document.getElementById('navbar-header');
    let navbarHeight = '10px';
    if (navbar.classList.contains('sticky-top') || navbar.classList.contains('fixed-top')) {
        navbarHeight = String(navbar.offsetHeight + 10) + 'px';
    }
    // Add to MathJax labels
    element.querySelectorAll('mjx-labels').forEach((label) => {
        label.querySelectorAll('mjx-mtd').forEach((number) => {
            number.style.setProperty('scroll-margin-top', navbarHeight);
        });
    });
    // Other blocks winthin element
    const blockTypes = ['blockquote', 'embed', 'figure', 'listing', 'table', 'cite'];
    blockTypes.forEach((blockType) => {
        element.querySelectorAll('.waggylabs-label-' + blockType).forEach((blockElem) => {
            blockElem.style.setProperty('scroll-margin-top', navbarHeight);
        });
    });
}

/**
 * Prepares wisuals sidebar tab
 * @param {DOM element} element - element within which blocks for sidebar will be processed
 */
function prepareSidebarVisuals(element) {
    // Citations are processed separately as they are in another sidebar tab
    // First process all types of blocks except equations
    const blockTypes = ['blockquote', 'embed', 'figure', 'listing', 'table'];
    blockTypes.forEach((blockType) => {
        element.querySelectorAll('.waggylabs-label-' + blockType).forEach((blockElem) => {
            const blockLabelElem = blockElem.querySelector('.waggylabs-entity-label');
            if (blockLabelElem) {
                // If label exists - update the labels in the sidebar blocks and modals
                const sb = document.getElementById('sb-' + blockLabelElem.id);
                const modal = document.getElementById('modal-' + blockLabelElem.id);
                if (sb) { sb.innerHTML = blockLabelElem.innerHTML; }
                if (modal) { modal.innerHTML = blockLabelElem.innerHTML; }
            }
        });
    });
    // Process equations
    element.querySelectorAll('.waggylabs-label-equation').forEach((eqElem) => {
        const eqLabelElem = eqElem.querySelector('.waggylabs-entity-label');
        if (eqLabelElem) {
            // If label exists - get the equation number generated by MathJax
            const numElem = eqElem.querySelector('mjx-labels').querySelector('mjx-mtext');
            if (numElem) {
                let eqNumber = '';
                // first and last children are opening and closing brackets, respectively
                for (let j = 1; j < numElem.children.length - 1; j++) {
                    eqNumber = eqNumber + numElem.children[j].classList[0].slice(-1);
                }
                if (eqNumber) {
                    eqLabelElem.innerHTML = eqLabelElem.innerHTML + ' ' + eqNumber + '.';
                }
            }
            const sb = document.getElementById('sb-' + eqLabelElem.id);
            const modal = document.getElementById('modal-' + eqLabelElem.id);
            if (sb) { sb.innerHTML = eqLabelElem.innerHTML; }
            if (modal) { modal.innerHTML = eqLabelElem.innerHTML; }
        }
    });
}

/**
 * Prepares sidebar table of contents
 * @param {DOM element} element - element from where to take headers
 */
function prepareSidebarContents(element) {
    // const toc = document.querySelector('.waggylabs-sidebar-toc');
    const headerTags = ['H1', 'H2', 'H3', 'H4', 'H5', 'H6'];
    const navbar = document.getElementById('navbar-header');
    var navbarHeight = '10px';
    if (navbar.classList.contains('sticky-top') || navbar.classList.contains('fixed-top')) {
        navbarHeight = String(navbar.offsetHeight + 10) + 'px';
    }

    document.querySelectorAll('.waggylabs-sidebar-toc').forEach((toc) => {
        element.childNodes.forEach((node, idx) => {
            if (headerTags.indexOf(node.tagName) >= 0) {
                node.setAttribute('id', 'waggylabs-header-' + String(idx));
                node.style.setProperty('scroll-margin-top', navbarHeight);
                var header_num = Number(node.tagName.slice(-1));
                var tocLink = document.createElement('a');
                tocLink.setAttribute('href', '#' + 'waggylabs-header-' + String(idx));
                tocLink.classList.add('nav-link', 'ms-2', 'ps-' + String(header_num - 1));
                tocLink.innerHTML = node.innerHTML;
                toc.appendChild(tocLink);
            }
        });
        if (!toc.parentNode.classList.contains('card-body') && !toc.parentNode.classList.contains('waggylabs-sidebar-tab-item')) {
            toc.appendChild(document.createElement('hr'));
        }
    });

    /* if (toc) {
        element.childNodes.forEach((node, idx) => {
            if (headerTags.indexOf(node.tagName) >= 0) {
                node.setAttribute('id', 'waggylabs-header-' + String(idx));
                node.style.setProperty('scroll-margin-top', navbarHeight);
                var header_num = Number(node.tagName.slice(-1));
                var tocLink = document.createElement('a');
                tocLink.setAttribute('href', '#' + 'waggylabs-header-' + String(idx));
                tocLink.classList.add('nav-link', 'ms-2', 'ps-' + String(header_num - 1));
                tocLink.innerHTML = node.innerHTML;
                toc.appendChild(tocLink);
            }
        });
    } */
}

/**
 * Prepares sidebar citations
 * @param {DOM element} element - element from where to take headers
 */
function prepareSidebarCitations(element) {
    // We need to select the last element of all literature elements
    // in case there is more than one on a post list page
    const literatureElems = element.querySelectorAll('.waggylabs-literature');
    const literatureElem = literatureElems[literatureElems.length - 1];
    // const literatureSidebarElem = document.querySelector('.waggylabs-sidebar-literature');
    if (literatureElem) {
        document.querySelectorAll('.waggylabs-sidebar-literature').forEach((lit) => {
            for (let i = 0; i < literatureElem.children.length; i++) {
                const citeClone = literatureElem.children[i].cloneNode(true);
                citeClone.children[0].removeAttribute('id');
                lit.appendChild(citeClone);
                if (i == literatureElem.children.length - 1) {
                    if (!lit.parentNode.classList.contains('card-body') && !lit.parentNode.classList.contains('waggylabs-sidebar-tab-item')) {
                        lit.appendChild(document.createElement('hr'));
                    }
                }
                else {
                    lit.appendChild(document.createElement('hr'));
                }
            }
        });
    }
    
    /* if (!literatureElem && literatureSidebarElem) {
        const noLiteratureElem = document.createElement('p');
        noLiteratureElem.innerHTML = 'No references found.';
        literatureSidebarElem.appendChild(noLiteratureElem);
    }
    if (literatureElem && literatureSidebarElem) {
        for (let i = 0; i < literatureElem.children.length; i++) {
            const citeClone = literatureElem.children[i].cloneNode(true);
            citeClone.children[0].removeAttribute('id');
            literatureSidebarElem.appendChild(citeClone);
            literatureSidebarElem.appendChild(document.createElement('hr'));
        }
    } */
}

function prepareSidebar(element) {
    prepareSidebarContents(element);
    prepareSidebarVisuals(element);
    prepareSidebarCitations(element);
}

function mathJaxPageReady() {
    let pageBodies = document.querySelectorAll('.waggylabs-page-body');
    // first process page bodies that come in list
    for (let i = 1; i < pageBodies.length; i++) {
        prepareReferences(pageBodies[i]);
        prepareCitations(pageBodies[i]);
        // MathJax.texReset([0]);
        MathJax.typeset([pageBodies[i]]);
        prepareScrollMarginTop(pageBodies[i]);
        MathJax.config.lastSectionNumber = MathJax.config.currentEquationNumber;
    }
    // finally process the main page body and sidebar
    prepareReferences(pageBodies[0]);
    prepareCitations(pageBodies[0]);
    MathJax.typeset([pageBodies[0]]);
    prepareScrollMarginTop(pageBodies[0]);
    const sidebar = document.getElementById('sidebar');
    if (sidebar) {
        MathJax.typeset([sidebar]);
        prepareSidebar(pageBodies[0]);
    }
    return new Promise((resolve, reject) => {});
}

function mathJaxReady() {
    const Configuration = MathJax._.input.tex.Configuration.Configuration;
    const CommandMap = MathJax._.input.tex.SymbolMap.CommandMap;
    new CommandMap('sections', {
        nextSection: 'NextSection',
        setSection: 'SetSection',
    }, {
        NextSection(parser, name) {
          MathJax.config.section++;
          parser.tags.counter = parser.tags.allCounter = 0;
        },
        SetSection(parser, name) {
          const n = parser.GetArgument(name);
          MathJax.config.section = parseInt(n);
        }
    });
    Configuration.create(
        'sections', {handler: {macro: ['sections']}}
    );
    MathJax.startup.defaultReady();
    MathJax.startup.input[0].preFilters.add(({math}) => {
        if (math.inputData.recompile) {
            MathJax.config.section = math.inputData.recompile.section;
        }
    });
    MathJax.startup.input[0].postFilters.add(({math}) => {
        if (math.inputData.recompile) {
            math.inputData.recompile.section = MathJax.config.section;
        }
    });
}