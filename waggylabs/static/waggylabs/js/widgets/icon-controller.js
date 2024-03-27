// waggylabs/static/js/icon-controller.js

class IconController extends window.StimulusModule.Controller {
    static values = { 
        // icons is object with keys: user-friedly icon name and values: bootstrap css class for icon element
        icons: Object,
    };

    connect() {
        const iconInput = document.getElementById(this.element.id);
        const clearButton = iconInput.nextElementSibling;

        const iconSpan = document.createElement("span");
        iconSpan.classList.add("autocomp");
        iconInput.parentNode.insertBefore(iconSpan, iconInput);

        if (clearButton) {
            clearButton.onclick = () => { 
                iconInput.value = '';
                iconSpan.innerHTML = '';
            };
        }

        iconInput.addEventListener("keyup", () => {
            if (iconInput.value.trim().length === 0) {
                iconSpan.innerHTML = '';
            }
        });

        if (iconInput.value && this.iconsValue[iconInput.value]) {
            iconSpan.innerHTML =  `<i class="${this.iconsValue[iconInput.value]}"></i>`;
        }

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
                if (this.iconsValue[val]) {
                    iconSpan.innerHTML =  `<i class="${this.iconsValue[val]}"></i>`;
                }
                return val;
            },
            onRender: (o) => {
                const sp = document.createElement("span");
                sp.innerHTML = `<i class="${this.iconsValue[o]}"></i>&nbsp;&nbsp;${o}`;
                return sp;
            },
        });
    }
}

window.wagtail.app.register('icon', IconController);