// waggylabs/static/js/icon-controller.js

class IconController extends window.StimulusModule.Controller {
    static values = { 
        // icons is object with keys: user-friedly icon name and values: bootstrap css class for icon element
        icons: Object,
    };

    connect() {
        const iconInput = document.getElementById(this.element.id); 
        const clearBtn = iconInput.nextElementSibling;
        // create
        autocomp(iconInput, {
            onQuery: async (val) => {
                // This callback returns an array of search results.
                // Typically, this will be a server side fetch() request.
                // Example:
                // const resp = await fetch(`/search?q=${query}`);
                // const res = await response.json();  
                // return res;
                const q = val.trim().toLowerCase();
                return Object.keys(this.iconsValue).filter(s => s.startsWith(q));
            },
            onSelect: (val) => {
                // Whatever is returned here is set in the input box.
                return val;
            },
            onRender: (o) => {
                const sp = document.createElement("span");
                sp.innerHTML = `<i class="${this.iconsValue[o]}"></i>&nbsp;${o}`;
                return sp;
            },
        });
    }
}

window.wagtail.app.register('icon', IconController);