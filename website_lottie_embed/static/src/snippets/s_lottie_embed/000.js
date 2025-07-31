/** @odoo-module **/ 

import publicWidget from "@web/legacy/js/public/public_widget";

const LottieEmbed = publicWidget.Widget.extend({
    selector: '.s_lottie_embed',
    disabledInEditableMode: false,

    /**
     * @override
     */
    start() {
        this._super.apply(this, arguments);
        const lottiePlayer = this.el.querySelector('lottie-player');
        const dataset = this.el.dataset;

        if (lottiePlayer) {
            lottiePlayer.load(dataset.lottieEmbed || '');
            lottiePlayer.speed = dataset.speed || "1";
            // The loop and autoplay attributes are boolean attributes, not value attributes.
            // We check for the string "true" because dataset values are always strings.
            if (dataset.loop === "true") {
                lottiePlayer.setAttribute('loop', '');
            } else {
                lottiePlayer.removeAttribute('loop');
            }
            if (dataset.autoplay === "true") {
                lottiePlayer.setAttribute('autoplay', '');
            } else {
                lottiePlayer.removeAttribute('autoplay');
            }
        }
    }
});

publicWidget.registry.LottieEmbed = LottieEmbed;

export default LottieEmbed;
