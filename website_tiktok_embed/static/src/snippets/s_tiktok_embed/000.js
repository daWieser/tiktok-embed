/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

const TiktokEmbed = publicWidget.Widget.extend({
    selector: ".s_tiktok_embed",
    disabledInEditableMode: false,

    /**
     * @override
     */
    start() {
        this.tiktokUrlStr = "https://www.tiktok.com/";
        const iframeEl = document.createElement("iframe");
        this.el.querySelector(".o_tiktok_container").appendChild(iframeEl);
        iframeEl.setAttribute("scrolling", "no");
        iframeEl.sandbox = "allow-popups allow-popups-to-escape-sandbox allow-scripts allow-top-navigation allow-same-origin";
        iframeEl.classList.add("w-100");
        iframeEl.height = "725px";
        // We have to setup the message listener before setting the src, because
        // the iframe can send a message before this JS is fully loaded.
        this.__onMessage = this._onMessage.bind(this);
        window.addEventListener("message", this.__onMessage);
        // We set the src now, we are ready to receive the message.
        iframeEl.src = `https://www.tiktok.com/embed/v2/${this._getTikTokVideoIdFromUrl(this.el.dataset.tiktokEmbed)}`;

        return this._super(...arguments);
    },

    _getTikTokVideoIdFromUrl(url) {
        const urlParameters = url.split(this.tiktokUrlStr)[1];
        const dirtyVideoId = urlParameters.split("/")[2]
        return dirtyVideoId.split("?")[0];
    },

    /**
     * @override
     */
    destroy() {
        const iframeEl = this.el.querySelector(".o_tiktok_container iframe");
        if (iframeEl) {
            iframeEl.remove();
            window.removeEventListener("message", this.__onMessage);
        }
        this._super.apply(this, arguments);
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * Called when a message is sent. Instagram sends us a message with the
     * height of the iframe.
     *
     * @private
     * @param {Event} ev
     */
    _onMessage(ev) {
        const iframeEl = this.el.querySelector(".o_tiktok_container iframe");
        if (ev.origin !== "https://www.tiktok.com" || iframeEl.contentWindow !== ev.source) {
            // It's not a message from Instagram or it's a message from another
            // Instagram iframe.
            return;
        }
    },
});

publicWidget.registry.TiktokEmbed = TiktokEmbed;

export default TiktokEmbed;
