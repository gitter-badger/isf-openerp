# -*- coding: utf-8 -*-

{
	'name': 'ISF Account module',
	'version': '0.2',
	'category': 'Tools',
	'description': """
Manage extended accounting
==========================
	
* add new types of data in the accounting module, such ascategories. 
* add district support for the customers
""",
	'author': 'Matteo Angelino (matteo.angelino@informaticisenzafrontiere.org)',
	'website': 'www.informaticisenzafrontiere.org',
	'license': 'AGPL-3',
	'depends': ['isf_district','sale','account'],
	'data': [
		'isf_account_view.xml',
		'res_partner_view.xml',
		],
	'demo': [],
	'installable' : True,
}

