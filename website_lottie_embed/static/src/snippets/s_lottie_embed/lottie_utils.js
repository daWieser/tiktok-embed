/** @odoo-module **/

/** Working public demo URL (do not use assets10 — returns 403). */
export const DEFAULT_LOTTIE_URL =
    "https://assets1.lottiefiles.com/packages/lf20_jcikwtux.json";

/**
 * @param {HTMLElement} containerEl
 * @returns {string}
 */
export function getLottieSrc(containerEl) {
    const fromDataset = containerEl.dataset.lottieEmbed;
    if (fromDataset && fromDataset !== "undefined") {
        return fromDataset;
    }
    const fromAttribute = containerEl.getAttribute("data-lottie-embed");
    if (fromAttribute && fromAttribute !== "undefined") {
        return fromAttribute;
    }
    return DEFAULT_LOTTIE_URL;
}

/**
 * @param {HTMLElement} containerEl
 * @returns {HTMLElement}
 */
export function getOrCreateLottiePlayer(containerEl) {
    let player = containerEl.querySelector("lottie-player");
    if (!player) {
        player = document.createElement("lottie-player");
        player.setAttribute("background", "transparent");
        player.setAttribute("width", "100%");
        player.setAttribute("height", "100%");
        player.classList.add("o_not_editable");
        const mountEl = containerEl.querySelector(".o_lottie_container") || containerEl;
        mountEl.appendChild(player);
    }
    return player;
}

/**
 * Load animation from data-lottie-embed (same path as the editor URL field).
 *
 * @param {HTMLElement} containerEl
 */
export async function syncLottiePlayer(containerEl) {
    if (!customElements.get("lottie-player")) {
        await customElements.whenDefined("lottie-player");
    }
    const dataset = containerEl.dataset;
    const player = getOrCreateLottiePlayer(containerEl);
    const src = getLottieSrc(containerEl);

    containerEl.dataset.lottieEmbed = src;
    // Do not set src attribute before load() — autoload can fail and show the error icon.
    player.removeAttribute("src");
    const loadResult = player.load(src);
    if (loadResult && typeof loadResult.then === "function") {
        await loadResult;
    }

    player.speed = dataset.speed || "1";

    if (dataset.loop === "true") {
        player.setAttribute("loop", "");
    } else {
        player.removeAttribute("loop");
    }
    if (dataset.autoplay === "true") {
        player.setAttribute("autoplay", "");
    } else {
        player.removeAttribute("autoplay");
    }
}
