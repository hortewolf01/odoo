from odoo import fields, models

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "The real estate property tag"
    _order = "name"

    name = fields.Char(
        required=True
    )
    color = fields.Integer()

    _sql_constraints = [
        ("name_uniq", "unique(name)", "Tag name must be unique!")
    ]