from odoo import fields, models

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "The real estate property type"

    name = fields.Char(
        required=True
    )

    _sql_constraints = [
        ("name_uniq", "unique(name)", "Type name must be unique!")
    ]
