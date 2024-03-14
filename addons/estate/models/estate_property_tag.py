from odoo import fields, models

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "The real estate property tag"

    name = fields.Char(
        required=True
    )

    _sql_constraints = [
        ("name_uniq", "unique(name)", "Tag name must be unique!")
    ]