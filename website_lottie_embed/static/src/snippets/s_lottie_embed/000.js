/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { syncLottiePlayer } from "./lottie_utils";

const LottieEmbed = publicWidget.Widget.extend({
    selector: ".s_lottie_embed",
    disabledInEditableMode: false,

    /**
     * @override
     */
    start() {
        const def = this._super.apply(this, arguments);
        return Promise.resolve(def).then(() => syncLottiePlayer(this.el));
    },
});

publicWidget.registry.LottieEmbed = LottieEmbed;

export default LottieEmbed;
