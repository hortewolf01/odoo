from odoo import models, fields, api, _
from odoo.exceptions import UserError
# import logging
# _logger = logging.getLogger(__name__)

class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "The real estate property offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False,
        readonly=True
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
    property_type_id = fields.Many2one(
        "estate.property.type",
        compute="_compute_property_type_id",
        store=True,
        readonly=True
    )

    _sql_constraints = [
        ("price_strictly_positive", "CHECK(price > 0)", "The price must be strictly positive.")
    ]

    @api.depends("validity")
    def _compute_date_deadline(self):
        for offer in self:
            create_date = offer.create_date or fields.Date.today()
            offer.date_deadline = fields.Date.add(create_date, days=offer.validity)
    
    def _inverse_date_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - offer.create_date.date()).days

    @api.depends("property_id.property_type_id")
    def _compute_property_type_id(self):
        for offer in self:
            offer.property_type_id = offer.property_id.property_type_id

    def action_set_accepted(self):
        for offer in self:
            if offer.status:
                raise UserError(_('Refused offers cannot be accepted.'))
            offer.status = 'accepted'
            property = offer.property_id
            property.buyer_id = offer.partner_id
            property.selling_price = offer.price
            other_offers = property.offer_ids.search([('id', '!=', offer.id)])
            for off in other_offers:
                off.status ='refused'
        return True

    def action_set_refused(self):
        for offer in self:
            offer.status ='refused'
        return True