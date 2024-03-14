from odoo import fields, models

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "The real estate property tag"

    name = fields.Char(
        required=True
    )