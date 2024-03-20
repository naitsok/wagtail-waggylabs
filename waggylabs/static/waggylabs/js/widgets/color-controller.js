// waggylabs/static/js/color-controller.js

class ColorController extends window.StimulusModule.Controller {
    static values = { 
        swatches: { type: Array, default: [] }, 
        theme: { type: String, default: 'pill' }, 
    };

    connect() {
        // create
        Coloris({ el: `#${this.element.id}` });

        // set options after initial creation
        setTimeout(() => {
            Coloris({ 
                swatches: this.swatchesValue,
                theme: this.themeValue,
                themeMode: 'auto',
                closeButton: true,
                clearButton: true,
                format: 'auto',
            });
        });
    }
}

window.wagtail.app.register('color', ColorController);