/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

const TiktokEmbed = publicWidget.Widget.extend({
    selector: ".s_tiktok_embed",
    disabledInEditableMode: true,

    start() {
        this.tiktokUrlStr = "https://www.tiktok.com/";
        const container = this.el.querySelector(".o_tiktok_container");
        const configLink = this.el.querySelector(".o_tiktok_url_config");
        let videoUrl = "https://www.tiktok.com/@mynfutebol/video/7327184434392747270";

        if (configLink && configLink.getAttribute("href") && configLink.getAttribute("href").includes("tiktok.com")) {
            videoUrl = configLink.getAttribute("href");
        } else if (this.el.dataset.tiktokEmbed) {
            videoUrl = this.el.dataset.tiktokEmbed;
        }

        const iframeEl = document.createElement("iframe");
        container.appendChild(iframeEl);

        iframeEl.setAttribute("scrolling", "no");
        iframeEl.sandbox = "allow-popups allow-popups-to-escape-sandbox allow-scripts allow-top-navigation allow-same-origin";
        iframeEl.classList.add("w-100");
        iframeEl.height = "725px";

        this.__onMessage = this._onMessage.bind(this);
        window.addEventListener("message", this.__onMessage);

        const videoId = this._getTikTokVideoIdFromUrl(videoUrl);
        if (videoId) {
            iframeEl.src = `https://www.tiktok.com/embed/v2/${videoId}`;
        }

        return this._super(...arguments);
    },

    _getTikTokVideoIdFromUrl(url) {
        try {
            if (!url.includes(this.tiktokUrlStr)) return null;
            const urlParameters = url.split(this.tiktokUrlStr)[1];
            const dirtyVideoId = urlParameters.split("/")[2]
            return dirtyVideoId.split("?")[0];
        } catch (e) {
            console.error("TikTok Embed: Invalid URL", url, e);
            return null;
        }
    },

    destroy() {
        const iframeEl = this.el.querySelector(".o_tiktok_container iframe");
        if (iframeEl) {
            iframeEl.remove();
            window.removeEventListener("message", this.__onMessage);
        }
        this._super.apply(this, arguments);
    },

    _onMessage(ev) {
        const iframeEl = this.el.querySelector(".o_tiktok_container iframe");
        if (ev.origin !== "https://www.tiktok.com" || iframeEl.contentWindow !== ev.source) {
            return;
        }
    },
});

publicWidget.registry.TiktokEmbed = TiktokEmbed;

export default TiktokEmbed;
