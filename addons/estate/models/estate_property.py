from odoo import fields, models, api

class Property(models.Model):
    _name = "estate.property"
    _description = "The real estate property"

    name = fields.Char(
        required=True
    )
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=fields.Date.add(fields.Date.today(), months=3) 
    )
    expected_price = fields.Float(
        required=True
    )
    selling_price = fields.Float(
        readonly=True,
        copy=False
    )
    bedrooms = fields.Integer(
        default=2
    )
    living_area = fields.Integer(
        string="Living Area (sqm)"
    )
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[('n', 'North'), ('s', 'South'), ('e', 'East'), ('w', 'West')]
    )
    active = fields.Boolean(
        default=True
    )
    state = fields.Selection(
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'), ('canceled', 'Canceled')],
        required=True,
        copy=False,
        default='new'
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Type"
    )
    buyer_id = fields.Many2one(
        "res.partner"
    )
    salesman_id = fields.Many2one(
        "res.users"
    )
    tag_ids = fields.Many2many(
        "estate.property.tag",
        string="Tags"
    )
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers"
    )
    total_area = fields.Float(
        compute="_compute_total_area",
        string="Total Area (sqm)"
    )
    best_price = fields.Float(
        compute="_compute_best_price"
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for property in self:
            offer_prices = property.offer_ids.mapped("price")
            if offer_prices:
                property.best_price = max(offer_prices)
            else:
                property.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 100
            self.garden_orientation = 'n'
        else:
            self.garden_area = None
            self.garden_orientation = None