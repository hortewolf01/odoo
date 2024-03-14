from odoo import models, fields, api
# import logging
# _logger = logging.getLogger(__name__)

class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "The real estate property offer"

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one(
        "res.partner",
        required=True
    )
    property_id = fields.Many2one(
        "estate.property",
        required=True
    )
    validity = fields.Integer(
        default=7,
        string="Validity (days)"
    )
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        string="Deadline"
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for offer in self:
            create_date = offer.create_date or fields.Date.today()
            offer.date_deadline = fields.Date.add(create_date, days=offer.validity)
    
    def _inverse_date_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - offer.create_date.date()).days