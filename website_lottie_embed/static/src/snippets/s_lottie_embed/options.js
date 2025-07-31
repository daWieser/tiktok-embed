/** @odoo-module **/

import options from '@web_editor/js/editor/snippets.options';

options.registry.LottieEmbed = options.Class.extend({
    /**
     * @override
     */
    init() {
        this._super(...arguments);
    },

    //--------------------------------------------------------------------------
    // Options
    //--------------------------------------------------------------------------

    async setLottieUpload(previewMode, widgetValue, params) {
        await new Promise(resolve => {
            const input = document.createElement('input');
            input.type = 'file';
            input.accept = '.json';
            input.onchange = async e => {
                const file = e.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = async (event) => {
                        try {
                            const lottieData = JSON.parse(event.target.result);
                            this.$target[0].dataset.lottieEmbed = 'data:application/json;base64,' + btoa(JSON.stringify(lottieData));
                            delete this.$target[0].dataset.lottieData; // Remove the old data attribute
                            await this._refresh();
                        } catch (error) {
                            console.error("Error parsing Lottie JSON:", error);
                            alert("Invalid Lottie JSON file.");
                        } finally {
                            resolve();
                        }
                    };
                    reader.readAsText(file);
                } else {
                    resolve();
                }
            };
            input.click();
        });
    },

    async setLottieEmbed(previewMode, widgetValue, params) {
        this.$target[0].dataset.lottieEmbed = widgetValue || "";
        this.$target[0].dataset.lottieData = ""; // Clear uploaded Lottie data when URL is set
        await this._refresh();
    },

    async setSpeed(previewMode, widgetValue, params) {
        this.$target[0].dataset.speed = widgetValue || "1";
        await this._refresh();
    },

    async setLoop(previewMode, widgetValue, params) {
        const currentValue = this.$target[0].dataset.loop === "true";
        this.$target[0].dataset.loop = (!currentValue).toString();
        await this._refresh();
    },

    async setAutoplay(previewMode, widgetValue, params) {
        const currentValue = this.$target[0].dataset.autoplay === "true";
        this.$target[0].dataset.autoplay = (!currentValue).toString();
        await this._refresh();
    },

    /**
     * Called when the transform button is clicked.
     */
    async transform() {
        this.trigger_up('hide_overlay');
        this.trigger_up('disable_loading_effect');

        const document = this.$target[0].ownerDocument;
        const playState = this.$target[0].style.animationPlayState;
        const transition = this.$target[0].style.transition;
        this.$target.transfo({document});
        const destroyTransfo = () => {
            this.$target.transfo('destroy');
            $(document).off('mousedown', mousedown);
            window.document.removeEventListener('keydown', keydown);
            this._refresh(); // Refresh snippet after transformation
        }
        const mousedown = mousedownEvent => {
            if (!$(mousedownEvent.target).closest('.transfo-container').length) {
                destroyTransfo();
                // Restore animation css properties potentially affected by the
                // jQuery transfo plugin.
                this.$target[0].style.animationPlayState = playState;
                this.$target[0].style.transition = transition;
            }
        };
        $(document).on('mousedown', mousedown);
        const keydown = keydownEvent => {
            if (keydownEvent.key === 'Escape') {
                keydownEvent.stopImmediatePropagation();
                destroyTransfo();
            }
        };
        window.document.addEventListener('keydown', keydown);

        await new Promise(resolve => {
            document.addEventListener('mouseup', resolve, {once: true});
        });
        this.trigger_up('enable_loading_effect');
    },

    /**
     * Called when the reset transform button is clicked.
     */
    async resetTransform() {
        this.$target.css({
            transform: '',
            width: '',
            height: '',
        });
        await this._refresh();
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @override
     */
    _computeWidgetState(widgetName, params) {
        if (widgetName === "setLottieEmbed") {
            return this.$target[0].dataset.lottieEmbed;
        } else if (widgetName === "setSpeed") {
            return this.$target[0].dataset.speed;
        } else if (widgetName === "setLoop") {
            return this.$target[0].dataset.loop === "true";
        } else if (widgetName === "setAutoplay") {
            return this.$target[0].dataset.autoplay === "true";
        }
        return this._super(...arguments);
    },

    /**
     * Restarts the public widget to apply all changes.
     * @private
     */
    async _refresh() {
        await this.trigger_up("widgets_start_request", {
            $target: this.$target,
            editableMode: true,
        });
    }
});

export default {
    LottieEmbed: options.registry.LottieEmbed,
};