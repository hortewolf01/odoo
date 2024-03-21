from odoo import fields, models, api

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "The real estate property type"
    _order = "name"

    name = fields.Char(
        required=True
    )
    property_ids = fields.One2many(
        "estate.property",
        "property_type_id",
        string="Properties"
    )
    sequence = fields.Integer()
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_type_id"
    )
    offer_count = fields.Integer(
        compute="_compute_offer_count"
    )

    _sql_constraints = [
        ("name_uniq", "unique(name)", "Type name must be unique!")
    ]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for type in self:
            type.offer_count = len(type.offer_ids)