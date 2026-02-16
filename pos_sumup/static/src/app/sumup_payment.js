/** @odoo-module */

import { _t } from "@web/core/l10n/translation";
import { PaymentInterface } from "@point_of_sale/app/payment/payment_interface";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

export class PaymentSumup extends PaymentInterface {
    setup() {
        super.setup(...arguments);
    }

    get fast_payments() {
        return true;
    }

    async send_payment_request(uuid) {
        await super.send_payment_request(uuid);
        return this._sumup_pay(uuid);
    }

    async send_payment_cancel(order, uuid) {
        await super.send_payment_cancel(order, uuid);
        return this._call_sumup({}, 'cancel');
    }

    pending_sumup_line() {
        return this.pos.getPendingPaymentLine("sumup");
    }

    _handle_odoo_connection_failure(data = {}) {
        var line = this.pending_sumup_line();
        if (line) {
            line.set_payment_status("retry");
        }
        this._show_error(
            _t(
                "Could not connect to the Odoo server, please check your internet connection and try again."
            )
        );
        return Promise.reject(data);
    }

    _call_sumup(data, operation = false) {
        return this.pos.data.silentCall(
            "pos.payment.method", 
            "proxy_sumup_request", 
            [
                [this.payment_method_id.id],
                data,
                operation,
            ]
        ).catch(this._handle_odoo_connection_failure.bind(this));
    }

    _sumup_pay_data(line) {
        var currency = this.pos.currency;
        var amount = line.amount;
        var minor_unit = currency.decimal_places;
        var value = Math.round(amount * Math.pow(10, minor_unit));

        return {
            "total_amount": {
                "value": value,
                "currency": currency.name,
                "minor_unit": minor_unit
            }
        };
    }

    _handle_sumup_error(error) {
        let msg = error.message;
        if (error.code === 'TIMEOUT') {
            msg = _t("The reader did not respond in time. Please try again.");
        } else if (error.code === 'NETWORK_ERROR') {
            msg = _t("Could not connect to SumUp. Check internet.");
        } else if (error.code === 'AUTH_ERROR') {
            msg = _t("Authentication failed. Check SumUp configuration.");
        }
        this._show_error(_t("SumUp Error: %s", msg));
    }

    _sumup_pay(uuid) {
        var order = this.pos.get_order();
        var line = order.payment_ids.find((paymentLine) => paymentLine.uuid === uuid);

        if (line.amount < 0) {
            this._show_error(_t("Cannot process transactions with negative amount."));
            return Promise.resolve();
        }

        var data = this._sumup_pay_data(line);
          
        return this._call_sumup(data, 'payment').then((response) => {
            if (response.error) {
                this._handle_sumup_error(response.error);
                line.set_payment_status("force_done");
                return false;
            }

            // Checkout created, start polling
            // The ID is in response.data.client_transaction_id
            var client_transaction_id = response.data && response.data.client_transaction_id;

            if (!client_transaction_id) {
                this._show_error(_t("SumUp Error: No client_transaction_id in response"));
                line.set_payment_status("retry");
                return false;
            }

            line.transaction_id = client_transaction_id; // Store for polling
            return this._poll_for_status(uuid, client_transaction_id);
        });
    }

    async _poll_for_status(uuid, client_transaction_id) {
        var line = this.pending_sumup_line();
        if (!line || line.uuid !== uuid) {
            return Promise.resolve(); // Payment cancelled or changed
        }

        // Poll every 3 seconds
        await new Promise(resolve => setTimeout(resolve, 3000));

        var data = { 'client_transaction_id': client_transaction_id };
        const response = await this._call_sumup(data, 'poll_status');

        if (response.error) {
            console.error("SumUp Poll Error", response.error);
            return this._poll_for_status(uuid, client_transaction_id);
        }

        var status = response.status;

        if (status === 'SUCCESSFUL') {
            line.set_payment_status("done");
            line.transaction_id = response.transaction_code || response.id || line.transaction_id;

            // Card details for receipt
            if (response.card) {
                line.card_type = response.card.type;
                line.cardholder_name = response.card.last_4_digits;
            }

            // Handle Tipping: if authorized amount > requested amount
            if (response.amount && response.amount > line.amount) {
                const tip_amount = response.amount - line.amount;
                if (this.pos.config.tip_product_id) {
                    await this.pos.set_tip(tip_amount);
                }
                line.set_amount(response.amount);
            }

            return true;
        } else if (status === 'FAILED') {
            this._show_error(_t("Payment failed."));
            line.set_payment_status("retry");
            return false;
        } else if (status === 'EXPIRED') {
            this._show_error(_t("Payment expired."));
            line.set_payment_status("retry");
            return false;
        } else if (status === 'PENDING') {
            return this._poll_for_status(uuid, client_transaction_id);
        } else {
            this._show_error(_t("Payment expired."));
        }
    }

    _show_error(msg, title) {
        if (!title) {
            title = _t("SumUp Error");
        }
        this.env.services.dialog.add(AlertDialog, {
            title: title,
            body: msg,
        });
    }
}
