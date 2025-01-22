from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        """Clear billing and shipping addresses only if the partner changes and the current values are invalid."""
        for record in self:
            if not record.partner_id:
                # If no partner is selected, clear the fields
                record.partner_invoice_id = False
                record.partner_shipping_id = False
            elif record.partner_id != self._origin.partner_id:
                # If the partner has changed, validate the existing addresses
                partner_child_ids = record.partner_id.child_ids.ids + [record.partner_id.id]
                # Retain the selected address if valid, otherwise clear
                if record.partner_invoice_id and record.partner_invoice_id.id not in partner_child_ids:
                    record.partner_invoice_id = False
                if record.partner_shipping_id and record.partner_shipping_id.id not in partner_child_ids:
                    record.partner_shipping_id = False
