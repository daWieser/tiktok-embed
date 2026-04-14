from odoo import fields, models, tools


class L10nAtWareneingangsbuchReport(models.Model):
    _name = "l10n_at.wareneingangsbuch.report"
    _description = "Austrian Wareneingangsbuch Report"
    _auto = False
    _order = "entry_date, invoice_reference, id"

    sequence_number = fields.Integer(
        string="Lfd. Nr.",
        readonly=True,
        group_operator=False,
    )
    entry_date = fields.Date(
        string="Tag des Waren-Eingangs / der Rechnungslegung",
        readonly=True,
    )
    receipt_date = fields.Date(string="Lieferdatum", readonly=True)
    invoice_date = fields.Date(string="Rechnungsdatum", readonly=True)
    supplier_id = fields.Many2one("res.partner", string="Lieferant", readonly=True)
    supplier_name = fields.Char(string="Lieferant", readonly=True)
    supplier_address = fields.Char(string="Anschrift des Lieferanten", readonly=True)
    supplier_display = fields.Char(string="Name und Anschrift des Lieferanten", readonly=True)
    goods_label = fields.Char(string="Produktbezeichnung", readonly=True)
    gross_amount = fields.Monetary(string="Brutto Betrag", readonly=True, currency_field="currency_id")
    net_amount = fields.Monetary(string="Netto Betrag", readonly=True, currency_field="currency_id")
    tax_amount = fields.Monetary(string="Vorsteuer", readonly=True, currency_field="currency_id")
    invoice_reference = fields.Char(
        string="Belegnummer der Einkaufsrechnung",
        readonly=True,
    )
    invoice_id = fields.Many2one("account.move", string="Einkaufsrechnung", readonly=True)
    invoice_line_id = fields.Many2one("account.move.line", string="Rechnungszeile", readonly=True)
    purchase_line_id = fields.Many2one("purchase.order.line", string="Bestellzeile", readonly=True)
    product_id = fields.Many2one("product.product", string="Produkt", readonly=True)
    product_tmpl_id = fields.Many2one("product.template", string="Produktvorlage", readonly=True)
    categ_id = fields.Many2one("product.category", string="Produktkategorie", readonly=True)
    currency_id = fields.Many2one("res.currency", string="Waehrung", readonly=True)
    company_id = fields.Many2one("res.company", string="Unternehmen", readonly=True)

    def action_open_invoice(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Einkaufsrechnung",
            "res_model": "account.move",
            "res_id": self.invoice_id.id,
            "view_mode": "form",
            "target": "current",
        }

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            f"""
            CREATE OR REPLACE VIEW {self._table} AS (
                WITH receipt_dates AS (
                    SELECT
                        sm.purchase_line_id,
                        MIN(sp.date_done::date) AS receipt_date
                    FROM stock_move sm
                    JOIN stock_picking sp ON sp.id = sm.picking_id
                    WHERE sm.purchase_line_id IS NOT NULL
                      AND sp.state = 'done'
                      AND sp.date_done IS NOT NULL
                    GROUP BY sm.purchase_line_id
                )
                SELECT
                    aml.id AS id,
                    ROW_NUMBER() OVER (
                        ORDER BY
                            COALESCE(rd.receipt_date, am.invoice_date, aml.date),
                            COALESCE(NULLIF(am.ref, ''), NULLIF(am.name, '')),
                            aml.id
                    )::integer AS sequence_number,
                    COALESCE(rd.receipt_date, am.invoice_date, aml.date) AS entry_date,
                    rd.receipt_date AS receipt_date,
                    am.invoice_date AS invoice_date,
                    partner.id AS supplier_id,
                    partner.name AS supplier_name,
                    TRIM(CONCAT_WS(', ',
                        NULLIF(TRIM(CONCAT_WS(' ', partner.street, partner.street2)), ''),
                        NULLIF(TRIM(CONCAT_WS(' ', partner.zip, partner.city)), ''),
                        country.code
                    )) AS supplier_address,
                    TRIM(CONCAT_WS(', ',
                        partner.name,
                        TRIM(CONCAT_WS(', ',
                            NULLIF(TRIM(CONCAT_WS(' ', partner.street, partner.street2)), ''),
                            NULLIF(TRIM(CONCAT_WS(' ', partner.zip, partner.city)), ''),
                            country.code
                        ))
                    )) AS supplier_display,
                    COALESCE(
                        NULLIF(pt.l10n_at_wareneingangsbuch_label, ''),
                        NULLIF(pc.l10n_at_wareneingangsbuch_label, ''),
                        NULLIF(REGEXP_REPLACE(aml.name, '^\\[[^]]+\\]\\s*', ''), '')
                    ) AS goods_label,
                    ABS(aml.price_total) AS gross_amount,
                    ABS(aml.price_subtotal) AS net_amount,
                    ABS(aml.price_total - aml.price_subtotal) AS tax_amount,
                    COALESCE(NULLIF(am.ref, ''), NULLIF(am.name, '')) AS invoice_reference,
                    am.id AS invoice_id,
                    aml.id AS invoice_line_id,
                    aml.purchase_line_id AS purchase_line_id,
                    aml.product_id AS product_id,
                    pp.product_tmpl_id AS product_tmpl_id,
                    pt.categ_id AS categ_id,
                    COALESCE(aml.currency_id, company.currency_id) AS currency_id,
                    aml.company_id AS company_id
                FROM account_move_line aml
                JOIN account_move am ON am.id = aml.move_id
                JOIN res_company company ON company.id = aml.company_id
                JOIN product_product pp ON pp.id = aml.product_id
                JOIN product_template pt ON pt.id = pp.product_tmpl_id
                JOIN product_category pc ON pc.id = pt.categ_id
                LEFT JOIN receipt_dates rd ON rd.purchase_line_id = aml.purchase_line_id
                LEFT JOIN res_partner partner ON partner.id = am.partner_id
                LEFT JOIN res_country country ON country.id = partner.country_id
                WHERE am.move_type = 'in_invoice'
                  AND am.state = 'posted'
                  AND COALESCE(aml.display_type, 'product') = 'product'
                  AND aml.product_id IS NOT NULL
                  AND pt.type IN ('product', 'consu')
                  AND pc.l10n_at_wareneingangsbuch_include = TRUE
            )
            """
        )
