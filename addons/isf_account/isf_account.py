from openerp.osv import fields, osv


class isf_account_customers_category(osv.osv):
	_name = "isf.account.customer.category"
	_description = "ISF account customers category"
	
	_columns = {
		'name' : fields.char('Category', size=20, required=True),
		'description' : fields.char('Category Description', size=100, required=True),
	}

_sql_constraints = [
        	('name', 'unique(name)', 'The code of the category must be unique')
    	]
	
isf_account_customers_category()

class isf_bill_type(osv.osv):
	_name = "isf.account.bill_type"
	_description = "ISF billing type"
	
	_columns = {
		'name' : fields.char('Bill code', size=20, required=True),
		'description' : fields.char('Bill type description', size=100, required=True),
	}

_sql_constraints = [
        	('name', 'unique(name)', 'The code of the bill must be unique')
    	]
	
isf_bill_type()


