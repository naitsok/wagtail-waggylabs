// waggylabs/static/js/icon-controller.js

class IconController extends window.StimulusModule.Controller {
    static values = { 
        icons: Array,
    };

    connect() {
        const cleaBtn = document.getElementById(this.element.id).nextSibling;
        // create
        const color = Coloris({ el: `#${this.element.id}` });

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

window.wagtail.app.register('icon', IconController);