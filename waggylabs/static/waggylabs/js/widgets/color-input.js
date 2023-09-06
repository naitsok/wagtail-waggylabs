
// Not needed for now because WidgetWithScript handles the initialization
// (() => {
//     window.addEventListener("DOMContentLoaded", () => {
//         createColorWidgets();
//     });
// })();


/**
 * Creates color widgets if they are not in StreamField
 * Not needed for now because WidgetWithScript handles the initialization
 */
function createColorWidgets() {
    var elements = document.querySelectorAll('input.waggylabs-color-input');
    var observedElements = [];

    for (let i = 0; i < elements.length; i++) {
        // Go through parent elements and check if there is streamfield container
        let current_el = elements[i];
        while (current_el.parentNode) {
            current_el = current_el.parentNode;
            if (current_el.hasAttribute('data-streamfield-stream-container')) {
                // We are inside streamfield - telepath will handle initialization
                break;
            }
            if (current_el.hasAttribute('role') && current_el.getAttribute('role') === 'tabpanel') {
                // We are inside a section and need to monitor its content and init 
                // additional widgets if they appear.
                colorAttach(elements[i].id);
                if (observedElements.indexOf(current_el.id) < 0) {
                    let observer = new MutationObserver(() => {
                        setTimeout(() => { 
                            updateColorWidgets(current_el.id); 
                        }, 50);
                    });
                    observer.observe(current_el, { 
                        childList: true,
                        subtree: true, 
                    });
                    observedElements.push(current_el.id);
                }
                break;
            }
        }
    }
}

/**
 * Update color widgets if more color inputs are dynamically added
 * Not needed for now because WidgetWithScript handles the initialization
 * @param {string} id - id of element inside which color widgets are updated
 */
function updateColorWidgets(id) {
    document.getElementById(id).querySelectorAll('input.waggylabs-color-input').forEach((el) => {
        colorAttach(el.id);
    });
}

/**
 * Attaches the color and opacity input elements to the hidden input associates with the\
 * database field
 */
function colorAttach(id) {

    const hidden = document.getElementById(id);
    if (!hidden.classList.contains('ui-color')) {
        const text = document.getElementById('text_' + hidden.name);
        const color = document.getElementById('color_' + hidden.name);
        const number = document.getElementById('number_' + hidden.name);
        const opacity = document.getElementById('opacity_' + hidden.name);
        const checkbox = document.getElementById('checkbox_' + hidden.name);

        function updateHidden () {
            hidden.value = 'rgba(' + parseInt(color.value.substr(1, 2), 16).toString() + ',' +
                parseInt(color.value.substr(3, 2), 16).toString() + ',' + 
                parseInt(color.value.substr(5, 2), 16).toString() + ',' +
                opacity.value + ')';
        }

        function enableInputs() {
            color.disabled = false;
            text.disabled = false;
            number.disabled = false;
            opacity.disabled = false;
        }

        function disableInputs() {
            color.disabled = true;
            text.disabled = true;
            number.disabled = true;
            opacity.disabled = true;
        }

        if (hidden.value) {
            let vals = hidden.value.replace(/rgba\(/g, '').replace(/\)/g, '').split(',');
            text.value = '#';
            for (let i = 0; i < 3; i++) {
                let hex = Number(vals[i]).toString(16);
                if (hex.length == 1) {
                    hex = '0' + hex;
                }
                text.value = text.value + hex;
            }
            opacity.value = vals[3];
            color.value = text.value;
            number.value = opacity.value;
            checkbox.checked = true;
        }
        else {
            // set some default values and disable inputs
            color.value = '#2b3035';
            opacity.value = 0.5;
            checkbox.checked = false;
            disableInputs();
        }

        text.addEventListener('change', () => { color.value = text.value; updateHidden(); });
        color.addEventListener('change', () => { text.value = color.value; updateHidden(); });
        number.addEventListener('change', () => { opacity.value = number.value; updateHidden(); });
        opacity.addEventListener('change', () => { number.value = opacity.value; updateHidden(); });
        opacity.addEventListener('input', () => { number.value = opacity.value; updateHidden(); });
        checkbox.addEventListener('change', () => {
            if (checkbox.checked) {
                enableInputs();
                updateHidden();
            }
            else {
                disableInputs();
                hidden.value = '';
            }
        });
        hidden.classList.add('ui-color');
    }
}