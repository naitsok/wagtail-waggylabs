// waggylabs/static/js/color-controller.js

class ColorController extends window.StimulusModule.Controller {
    static values = { 
        swatches: { type: Array, default: [] }, 
        theme: { type: String, default: 'pill' },
        themeMode: { type: String, default: 'auto' },
        closeButton: { type: Boolean, default: true },
        clearButton: { type: Boolean, default: true },
        formatToggle: { type: Boolean, default: true },
    };

    connect() {
        const colorInput = document.getElementById(this.element.id);
        const clearButton = colorInput.nextElementSibling;
        if (clearButton) {
            clearButton.onclick = () => { 
                colorInput.value = '';
                colorInput.dispatchEvent(new Event('input', { bubbles: true }));
            };
        }
        // create
        Coloris({ el: `#${this.element.id}` });

        // set options after initial creation
        setTimeout(() => {
            Coloris({ 
                swatches: this.swatchesValue,
                theme: this.themeValue,
                themeMode: this.themeModeValue,
                closeButton: this.closeButtonValue,
                clearButton: this.clearButtonValue,
                formatToggle: this.formatToggleValue,
            });
        });
    }
}

window.wagtail.app.register('color', ColorController);