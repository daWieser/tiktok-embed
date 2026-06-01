# -*- coding: utf-8 -*-
from odoo import api, models, _


class ReportSaleDetailsTaxIds(models.AbstractModel):
    _inherit = 'report.point_of_sale.report_saledetails'

    def _get_products_and_taxes_dict(self, line, products, taxes, currency):
        products, taxes = super()._get_products_and_taxes_dict(line, products, taxes, currency)
        tax_cache = self.env.context.get('sale_details_tax_cache')
        if tax_cache is not None:
            category_name = (
                line.product_id.product_tmpl_id.pos_categ_ids[0].name
                if line.product_id.product_tmpl_id.pos_categ_ids
                else _('Not Categorized')
            )
            key = (category_name, line.product_id.id, line.price_unit, line.discount)
            tax_name = ', '.join(line.tax_ids_after_fiscal_position.mapped('name')) or _('No Taxes')
            tax_cache.setdefault(key, set()).add(tax_name)
        return products, taxes

    def _assign_tax_ids(self, categories, tax_cache):
        for category in categories:
            for line in category.get('products', []):
                key = (category['name'], line['product_id'], line['price_unit'], line['discount'])
                line['tax_id'] = ', '.join(sorted(tax_cache.get(key, []))) or _('No Taxes')

    @api.model
    def get_sale_details(self, date_start=False, date_stop=False, config_ids=False, session_ids=False, **kwargs):
        tax_cache = {}
        result = super(ReportSaleDetailsTaxIds, self.with_context(sale_details_tax_cache=tax_cache)).get_sale_details(
            date_start=date_start,
            date_stop=date_stop,
            config_ids=config_ids,
            session_ids=session_ids,
            **kwargs,
        )
        self._assign_tax_ids(result.get('products', []), tax_cache)
        self._assign_tax_ids(result.get('refund_products', []), tax_cache)
        return result
