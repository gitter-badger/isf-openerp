from openerp.osv import fields, osv

class res_partner(osv.osv):
	_description = "ISF Partner"
	_inherit = "res.partner"
	
	_columns = {
		'district_ids' : fields.many2one('isf.district.district','code',required=True),
		'zone_ids' : fields.many2one('isf.district.zone', "code",domain="[('district_ids', '=', district_ids)]",required=True),
		'subzone_ids' : fields.many2one('isf.district.subzone',"code",domain="[('zone_ids', '=', zone_ids)]",required=True),
		'location_ids' : fields.many2one('isf.district.block','name',required=True,domain="['&',('district_ids', '=', district_ids),'&',('zone_ids', '=', zone_ids),('subzone_ids', '=', subzone_ids)]"),
		'land_ids' : fields.many2many('isf.district.plot','res_partner_land_rel','partner_id','code','Plot Number',domain="[('block_ids', '=', location_ids)]"),
		'build_ids' : fields.many2many('isf.district.plot','res_partner_build_rel','partner_id','code','Plot Number',domain="[('block_ids', '=', location_ids)]"),
		'category_ids' : fields.many2one('isf.account.customer.category','category',required=True),
		'bill_to_ids' : fields.many2one('res.partner','partner_id'),
		'customer_number' : fields.char('Customer number',size=12,required=True),
		'bill_type_ids' : fields.many2one('isf.account.bill_type','name',required=True),
		'tariff_code_ids' : fields.many2one('account.tax','name',required=False),
	}
	
	def copy(self, cr, uid, record_id, default=None, context=None):
		if default is None:
			default = {}

		default['plot_ids'] = []
		return super(res_partner, self).copy(
			cr, uid, record_id, default=default, context=context)
			
	
res_partner()