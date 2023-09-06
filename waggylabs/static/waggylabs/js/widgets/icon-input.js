/**
 * Initializes icon input widgets on any admin page and monitors
 * for the DOM content changes and initalizes newly added icon
 * input widgets.
 * 
 * When icon input widget is used as a standalone widget, it needs to be
 * initialized when DOM is loaded, because telepath in this case is not
 * available. 
 */

//  Not needed for now because WidgetWithScript handles the initialization
// (() => {
//     window.addEventListener("DOMContentLoaded", () => {
//         createAutocompleteWidgets();
//     });
// })();


/**
 * Not needed for now because WidgetWithScript handles the initialization
 * Creates autocomplete widgets if they are not in StreamField
 */
function createAutocompleteWidgets() {
    var elements = document.querySelectorAll('input.waggylabs-icon-input');
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
                autocompleteAttach(elements[i].id);
                if (observedElements.indexOf(current_el.id) < 0) {
                    let observer = new MutationObserver(() => {
                        setTimeout(() => { 
                            updateAutocompleteWidgets(current_el.id); 
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
 * Not needed for now because WidgetWithScript handles the initialization
 * Updates autocomplete widgets if more autocomplete inputs are dynamically added
 * @param {string} id - id of element inside which autocomplete widgets are updated
 */
function updateAutocompleteWidgets(id) {
    document.getElementById(id).querySelectorAll('input.waggylabs-icon-input').forEach((el) => {
        autocompleteAttach(el.id);
    });
}

/**
 * Function to attach the JQuery UI autocomplete widget
 * @param {string} id - id of the text input for the widget attachment
 */
function autocompleteAttach(id) {
    var element = $('#' + id);
    if (!$(element).hasClass("ui-autocomplete-input")) {
        var icons = JSON.parse($(element).attr("iconsjson"));
        if ($(element).val()) {
            $(`<i class="w-field__icon ${icons[$(element).val()]}"></i>`).insertBefore($(element));
        }
        $(element).autocomplete({
            source: Object.keys(icons),
            select: (event, ui) => {
                $(element).val(ui.item.label);
                $(element).parent().find("i").remove();
                $(`<i class="w-field__icon ${icons[ui.item.label]}"></i>`).insertBefore($(element));
                return false;
            },
        }).data("ui-autocomplete")._renderItem = (ul, item) => {
            return $("<li></li>")
                .data("item.autocomplete", item)
                .append(`<i class="${icons[item.label]}"></i>&nbsp;${item.label}`)
                .appendTo(ul);
        };
    }
}