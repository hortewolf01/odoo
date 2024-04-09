from odoo import models
from odoo.fields import Command

class Property(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        for property in self:
            self.env['account.move'].create(
                {
                    'partner_id': property.buyer_id.id,
                    'move_type': 'out_invoice',
                    'invoice_line_ids': [
                        Command.create({'name': '6% of the selling price',
                                        'quantity': 1,
                                        'price_unit': property.best_price * 0.06}),
                        Command.create({'name': 'Administrative fees',
                                        'quantity': 1,
                                        'price_unit': 100})
                    ]
                }
            )
        super().action_set_sold()
        return True