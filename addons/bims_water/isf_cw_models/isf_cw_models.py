from openerp.osv import osv, fields
import logging
import time

_logger = logging.getLogger("CW")

class isf_cw_zone(osv.osv):
    """ Zone - cw.zones """
    _name = "isf.cw.zone"
    _description = "Zone"
    _columns = {
        'code' : fields.char('Code', size=50, required=True),
        'name' : fields.char('Name', size=50, required=True),
        'active' : fields.boolean('Active'),
        'partner_ids': fields.many2many('res.partner', 'res_partner_zone_rel', 'partner_id', 'zone_id', 'Contacts'),
        'areas_id': fields.one2many('isf.cw.zone.area', 'zone_id', 'Zone Areas'),
        'meterreader_id': fields.many2many('hr.employee', 'isf_cw_meterreader_zone_rel', 'employee_id', 'zone_id', 'Meter reader'),
    }
    _defaults = {
        'active': True
    }
    _sql_constraints = [
        ('zone_uniq', 'unique(code)', 'Zone code must be unique'),
    ]

isf_cw_zone()

class isf_cw_area(osv.osv):
    """ Area - cw.area """
    _name = "isf.cw.zone.area"
    _description = "Area"
    _columns = {
        'code' : fields.char('Code', size=50, required=True),
        'name' : fields.char('Name', size=50, required=True),
        'max_connections' : fields.integer('Max Connections', required=True),
        'zone_id' : fields.many2one('isf.cw.zone', 'Zone'),
    }
    _sql_constraints = [
        ('area_uniq', 'unique(code,zone_id)', 'Code already present'),
    ]

isf_cw_area()

class isf_cw_flowmeter_type(osv.osv):
    """ Flow Meter Type - cw.flowmeter.metername normalization """
    _name = "isf.cw.flowmeter.type"
    _description = "Flow Meter Type"
    _columns = {
        'name' : fields.char('Meter Type', size=50, required=True),
        'unit_id' : fields.many2one('product.uom', 'Unit of Measure', required=True), 
    }
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Group name must be unique'),
    ]

isf_cw_flowmeter_type()

class isf_cw_flowmeter(osv.osv):
    """ Flow Meter (Device) - cw.flowmeter """
    _name = "isf.cw.flowmeter"
    _description = "Flow Meter Device"
    _columns = {
        'name' : fields.char('MeterNo', size=50, required=True),
        'type' : fields.many2one('isf.cw.flowmeter.type', 'Meter Type', required=True),
        'parent_id' : fields.many2one('isf.cw.flowmeter', 'Parent Meter'),
        'child_ids': fields.one2many('isf.cw.flowmeter', 'parent_id', 'Child Ids'),
        'level' : fields.integer('Level'),
        'date' : fields.date('Date'),
        'active' : fields.boolean('Active'),
        'streading' : fields.integer('ST Readings'),
        'current_customer': fields.many2one('res.partner', "Current Customer", domain="[('customer','=',True)]"),
        #'unit_id' : fields.many2one('product.uom', 'Unit of Measure', required=True), 
    }
    _defaults = {
        'level': 0,
        'active': 0,
        'streading': 0,
        'date': lambda *a: time.strftime('%Y-%m-%d'),
    }
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Meter Number must be unique'),
    ]

isf_cw_flowmeter()

#class isf_charge(osv.osv):
#    """ Charges - cw.charges """
#    _inherit = "product.product"
#
#isf_charge()

class isf_cw_customergroup(osv.osv):
    """ Customer Groups - cw.cgroups """
    _inherit = "res.partner.category"
    _columns = {
        'currency_id': fields.many2one('res.currency', 'Currency', required=False),
        #'charge': fields.many2many('product.product', 'Charge', required=False, domain="['category','=','charges']"),
        'charge_id': fields.many2many('product.product', 'isf_cw_customergroup_charge_rel', 'product_id', 'category_id', 'Charges'),
        'tariff_id' : fields.one2many('isf.cw.tariff', 'partner_category_id', 'Assigned Tariff', required=False)
    }

isf_cw_customergroup()

class isf_meter_owner(osv.osv):
    """ Meter Owner History """
    _name = "isf.cw.meter.owner"
    _columns = {
        'partner_id': fields.many2one("res.partner", "Customer", required=True, domain="['|',('customer','=',True),('employee','=',True)]"),
        'flow_meter': fields.many2one("isf.cw.flowmeter", "Meter", required=True),
        'startdate': fields.date("Start Date"),
        'enddate': fields.date("Start Date"),
    }
    _defaults = {
        'startdate': lambda *a: time.strftime('%Y-%m-%d'),
    }
 
isf_meter_owner()

#domain="['|',('customer','=',True),('employee','=',True)]"
class isf_cw_customer(osv.osv):
    """ Customer - cw.customer """
    _inherit = "res.partner"
    _columns = {
        'area_id' : fields.many2one('isf.cw.zone.area', "Area", domain="[('zone_id', '=', zone_id)]"),
        'zone_id': fields.related(
            'area_id',
            'zone_id',
            type="many2one",
            relation="isf.cw.zone",
            string="Zone",
            store=True
        ),
        'supplyno': fields.many2one('isf.cw.supply', "Current Furniture", required=False),
    }

isf_cw_customer()

class isf_cw_supply(osv.osv):
    _name = "isf.cw.supply"
    _columns = {
        'area_id' : fields.many2one('isf.cw.zone.area', "Area", domain="[('zone_id', '=', zone_id)]"),
        'zone_id': fields.related(
            'area_id',
            'zone_id',
            type="many2one",
            relation="isf.cw.zone",
            string="Zone",
            store=True
        ),
        'supplyno' : fields.char('Supply Number', size=32, readonly=True, states={'draft':[('readonly',False)]}),
        'plumber': fields.many2one('hr.employee', "Plumber", domain=[('job_id', 'ilike', 'Plumber')]),
        'flow_meter': fields.many2one('isf.cw.flowmeter', "Current Flow Meter"),
        'partner_id': fields.many2one('res.partner', 'Customer', required=True, domain=[('customer','=',True)]),
        'assigned_date': fields.date("Assigned Date"),
        'state': fields.selection([('draft', 'Draft'), ('validation', 'Validation'), ('active', 'Active'), ('suspended','Suspended'), ('blocked', 'Blocked'), ('terminated', 'Terminated')], 'Status'),
        'notes': fields.text("Notes")
    }
    _defaults = {
        'supplyno': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'isf.cw.supply'),
        'state': 'draft'
    }
    _sql_constraints = [
        ('zone_supplyno_uniq', 'unique(zone_id, supplyno)', 'Supplier id already existing in zone'),
    ]

isf_cw_supply()

"""
        'area_id' : fields.many2many('isf.cw.zone.area', "Area"),
        'zone_id': fields.related(
            'area_id',
            'zone_id',
            type="many2one",
            relation="isf.cw.zone",
            string="Zone",
            store=False),
"""

class isf_cw_meterreader(osv.osv):
    #_inherits = {
    #    'hr.employee': 'employee_id',
    #}
    _inherit = "hr.employee"
    #_name = "isf.cw.meterreader"
    _columns = {
        'zone_id': fields.many2many('isf.cw.zone', 'isf_cw_meterreader_zone_rel', 'zone_id', 'employee_id', 'Zones'),
        #'employee_id': fields.many2one('hr.employee',
        #    string='Related Employee', ondelete='restrict',
        #    help='Employee-related data of the meter reader'),
    }

    #def onchange_company(self, cr, uid, ids, company, context=None):
    #    return super(isf_cw_meterreader, self).onchange_company(cr, uid, ids, company, context)


isf_cw_meterreader()

class isf_cw_reading(osv.osv):
    _name = "isf.cw.flowmeter.reading"
    def on_change_partner_id(self, cr, uid, ids, partner_id, context=None):
        last_reading = 0
        if partner_id:
            reading_id = self.search(cr, uid, [('partner_id', '=', partner_id)], context=context)
            last_reading = self.read(cr, uid, reading_id, fields=["value"], context=context)[0]['value']
        return {'value': {'last_reading': last_reading}}

    def _get_last_reading(self, cr, uid, ids, field_name, arg, context=None):
        last_reading = 0
        if self.partner_id:
            last_reading = self.on_change_partner_id(cr, uid, partner_id=self.partner_id,  context=context)['value']['last_reading']
        return last_reading

    def _on_change_value(self, cr, uid, ids, value, context=None):
        units = 0
        if value:
            last_reading = self.on_change_partner_id(cr, uid, partner_id=self.partner_id,  context=context)['value']['last_reading']
            units = value - units
        return {'value': {'units': units}}

    _columns = {
        #'supplyno': fields.many2one('isf.cw.supply', "Supply Number", required=False),
        'partner_id': fields.many2one('res.partner', 'Customer', required=True, domain=[('customer','=',True)]),
        'flow_meter': fields.many2one('isf.cw.flowmeter', "Current Flow Meter"),
        'meter_reader': fields.many2one('hr.employee', "Meter Reader", domain=[('job_id', 'ilike', 'Meter Reader')]),
        'date': fields.date("Reading Date"),
        'is_monthly': fields.boolean("Monthly"),
        'value' : fields.integer('Reading Value', size=11, required=True),
        'units' : fields.integer('Bill Units', size=11, required=True, , states={'defective':[('readonly',False)]}),
        'state': fields.selection([('draft', 'Draft'), ('defective', 'Defective')], 'Status'),
        'last_reading': fields.function(_get_last_reading, type='integer', string='Last Reading', store=False),
        'defective': fields.boolean("Defective"),
        'insert_date': fields.date("Insert Date"),
        'notes': fields.text("Notes")
    }

isf_cw_reading()

import openerp.addons.decimal_precision as dp

class isf_cw_tariff_range(osv.osv):
    _name = "isf.cw.tariff.range"
    def _get_unit_precision(self, cr, uid, ids, field_name, arg, context=None):
        # @TODO: lookup tariff currency
        _logger.info("_get_unit_precision: %s" % str([ids, field_name, arg, context])) 
        return (6,2)

    _columns = {
        'tariff_id': fields.many2one('isf.cw.tariff', 'Tariff', required=True),
        'from': fields.integer("From", size=11, required=True),
        'to': fields.integer("To", size=11, required=True),
        'price_unit': fields.float('Unit Price', required=True, readonly=False),
    }
 
isf_cw_tariff_range()

class isf_cw_tariff(osv.osv):
    _name = "isf.cw.tariff"

    def _get_currency(self, cr, uid, ctx):
        comp = self.pool.get('res.users').browse(cr, uid, uid).company_id
        if not comp:
            comp_id = self.pool.get('res.company').search(cr, uid, [])[0]
            comp = self.pool.get('res.company').browse(cr, uid, comp_id)
        return comp.currency_id.id

    _columns = {
        'name' : fields.char('Name', size=50, required=True),
        'state': fields.selection([
            ('draft','Draft'),
            ('suspended','Suspended'),
            ('active','Active'),
            ], 'Status', required=True, track_visibility='onchange',
            help='When a tarif is created the status is set to \'Draft\'.\n If the tariff is connected to a bill, the status is set to \'Active\' and the tariff cannot be modified.'),
        'unit_id' : fields.many2one('product.uom', 'Unit of Measure', required=True), 
        'currency_id': fields.many2one('res.currency', 'Currency', required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'partner_category_id': fields.many2one('res.partner.category', 'Customer Groups', required=False),
        'range_ids': fields.one2many('isf.cw.tariff.range', 'tariff_id', "Tariff Ranges"),
        'notes': fields.text("Notes")
    }

    _defaults = {
        "currency_id": _get_currency,
        'state': 'draft'
    }

isf_cw_tariff()
