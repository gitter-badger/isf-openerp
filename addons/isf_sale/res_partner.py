from openerp.osv import fields, osv

class res_partner(osv.osv):
	_description = "ISF Sale Partner"
	_inherit = "res.partner"
	
	_columns = {
		'plot_ids' : fields.many2many('district.plot','res_partner_plot_rel','partner_id','code','Plot Number'),
		'category_ids' : fields.many2one('isf_sale.customer.category','category',required=True),
	}
	
	def copy(self, cr, uid, record_id, default=None, context=None):
		if default is None:
			default = {}

		default['plot_ids'] = []
		return super(res_partner, self).copy(
			cr, uid, record_id, default=default, context=context)
			
	
res_partner()