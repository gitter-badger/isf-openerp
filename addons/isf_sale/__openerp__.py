# -*- coding: utf-8 -*-

{
	'name': 'ISF Sales module',
	'version': '0.1',
	'category': 'Tools',
	'description': """ISF Sales extension (District support)""",
	'author': 'Matteo Angelino (matteo.angelino@informaticisenzafrontiere.org)',
	'website': 'www.informaticisenzafrontiere.org',
	'license': 'AGPL-3',
	'depends': ['district','sale','account'],
	'data': [
		'isf_sale_view.xml',
		'res_partner_view.xml',
		],
	'demo': [],
	'installable' : True,
}

