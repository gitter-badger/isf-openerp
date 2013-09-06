from openerp.osv import fields, osv

class isf_sale_order(osv.osv):
	_name = "isf_sale.order"
	_description = "ISF Sale order (District support)"
	_inherit = "sale.order"
	
	_columns = {
		'district' : fields.char('District', size=100, required=True),
	}
	
isf_sale_order()

class isf_sale_customers_category(osv.osv):
	_name = "isf_sale.customer.category"
	_description = "ISF Sale customers category"
	
	_columns = {
		'category' : fields.char('Category', size=20, required=True),
		'description' : fields.char('Category Description', size=100, required=True),
	}


