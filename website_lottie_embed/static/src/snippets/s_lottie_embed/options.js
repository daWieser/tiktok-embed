/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Plugin } from "@html_editor/plugin";
import { withSequence } from "@html_editor/utils/resource";
import { BuilderAction } from "@html_builder/core/builder_action";
import { SNIPPET_SPECIFIC_END } from "@html_builder/utils/option_sequence";
import { BaseOptionComponent } from "@html_builder/core/utils";
import { _t } from "@web/core/l10n/translation";
import { getLottieSrc, syncLottiePlayer } from "./lottie_utils";

function reloadLottie(editingElement) {
    syncLottiePlayer(editingElement).catch((error) => {
        console.error("Lottie embed: failed to load animation", error);
    });
}

// 1. Action to handle file upload
class LottieUploadAction extends BuilderAction {
    static id = "lottieUpload";

    async load() {
        let newContent;
        await new Promise((resolve) => {
            const input = document.createElement("input");
            input.type = "file";
            input.accept = ".json";
            input.onchange = (e) => {
                const file = e.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = (event) => {
                        try {
                            const lottieData = JSON.parse(event.target.result);
                            newContent =
                                "data:application/json;base64," +
                                btoa(JSON.stringify(lottieData));
                        } catch (error) {
                            console.error("Error parsing Lottie JSON:", error);
                            this.services.notification.add(_t("Invalid Lottie JSON file."), {
                                type: "danger",
                            });
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
        return newContent;
    }

    apply({ editingElement, loadResult: content }) {
        if (!content) {
            return;
        }
        editingElement.dataset.lottieEmbed = content;
        reloadLottie(editingElement);
    }
}

// 2. Action to handle URL setting
class LottieUrlAction extends BuilderAction {
    static id = "lottieUrl";
    getValue({ editingElement }) {
        return getLottieSrc(editingElement);
    }
    apply({ editingElement, value }) {
        editingElement.dataset.lottieEmbed = value || "";
        reloadLottie(editingElement);
    }
}

// 3. Action to handle Speed setting
class LottieSpeedAction extends BuilderAction {
    static id = "lottieSpeed";
    getValue({ editingElement }) {
        return editingElement.dataset.speed || "1";
    }
    apply({ editingElement, value }) {
        editingElement.dataset.speed = value || "1";
        reloadLottie(editingElement);
    }
}

// 4. Action to handle Loop checkbox
class LottieLoopAction extends BuilderAction {
    static id = "lottieLoop";
    getValue({ editingElement }) {
        return editingElement.dataset.loop === "true";
    }
    apply({ editingElement, value }) {
        editingElement.dataset.loop = value ? "true" : "false";
        reloadLottie(editingElement);
    }
}

// 5. Action to handle Autoplay checkbox
class LottieAutoplayAction extends BuilderAction {
    static id = "lottieAutoplay";
    getValue({ editingElement }) {
        return editingElement.dataset.autoplay === "true";
    }
    apply({ editingElement, value }) {
        editingElement.dataset.autoplay = value ? "true" : "false";
        reloadLottie(editingElement);
    }
}

// 6. OWL Option Component
export class LottieEmbedOption extends BaseOptionComponent {
    static template = "website_lottie_embed.LottieEmbedOption";
    static selector = ".s_lottie_embed";
}

// 7. Option Plugin
class LottieEmbedOptionPlugin extends Plugin {
    static id = "lottieEmbedOptionPlugin";

    setup() {
        this.onSnippetDropped = this.onSnippetDropped.bind(this);
    }

    onSnippetDropped({ snippetEl }) {
        if (snippetEl.matches(".s_lottie_embed")) {
            reloadLottie(snippetEl);
        }
    }

    /** @type {import("plugins").WebsiteResources} */
    resources = {
        builder_options: [withSequence(SNIPPET_SPECIFIC_END, LottieEmbedOption)],
        so_content_addition_selector: [".s_lottie_embed"],
        builder_actions: {
            LottieUploadAction,
            LottieUrlAction,
            LottieSpeedAction,
            LottieLoopAction,
            LottieAutoplayAction,
        },
        on_snippet_dropped_handlers: ({ snippetEl }) => this.onSnippetDropped({ snippetEl }),
    };
}

registry.category("website-plugins").add(LottieEmbedOptionPlugin.id, LottieEmbedOptionPlugin);
