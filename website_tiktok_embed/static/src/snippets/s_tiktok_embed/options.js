/** @odoo-module **/

import {_t} from "@web/core/l10n/translation";
import options from "@web_editor/js/editor/snippets.options";

options.registry.TiktokEmbed = options.Class.extend({
    /**
     * @override
     */
    init() {
        this._super(...arguments);
        this.orm = this.bindService("orm");
        this.notification = this.bindService("notification");
    },

    //--------------------------------------------------------------------------
    // Options
    //--------------------------------------------------------------------------

    /**
     * Registers the instagram page name.
     *
     * @see this.selectClass for parameters
     */
    async setTiktokEmbed(previewMode, widgetValue, params) {
        this.$target[0].dataset.tiktokEmbed = widgetValue || "";
        // As the public widget restart is disabled for instagram, we have to
        // manually restart the widget.
        await this.trigger_up("widgets_start_request", {
            $target: this.$target,
            editableMode: true,
        });
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @override
     */
    _computeWidgetState(widgetName, params) {
        if (widgetName === "setTiktokEmbed") {
            return this.$target[0].dataset.tiktokEmbed;
        }
        return this._super(...arguments);
    },
});

export default {
    TiktokEmbed: options.registry.TiktokEmbed,
};
