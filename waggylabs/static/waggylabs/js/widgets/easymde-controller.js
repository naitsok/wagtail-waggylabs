// waggylabs/static/js/easymde-controller.js

class EasyMDEContainer extends window.StimulusModule.Controller {
    static values = { 
        autodownload: { type: Boolean, default: true },
        minHeight: { type: String, default: "300px" },
        maxHeight: { type: String, default: "300px" },
        stexCombine: { type: Boolean, default: true },
        toolbar: { type: String, default: "bold,italic,strikethrough,heading,|,unordered-list,ordered-list,link,|,code,subscript,superscript,equation,matrix,align,|,preview,side-by-side,fullscreen,guide" },
        statusbar: { type: Boolean, default: true },
    };

    connect() {
        easymdeAttach(this.element.id, this.autodownloadValue, this.minHeightValue, this.maxHeightValue, this.stexCombineValue, this.toolbarValue, this.statusbarValue);
    }
}

window.wagtail.app.register("easymde", EasyMDEContainer);