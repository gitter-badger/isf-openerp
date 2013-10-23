# -*- coding: utf-8 -*-

{
	'name': 'ISF bank transfer form',
	'version': '0.2',
	'category': 'Tools',
	'description': """

ISF Bank transfer form
======================
	
* Add a new wizard to perform bank transfer
* All bank transfer are performed on special journal bank operation
* Setting special journal with new flag Bank operations in journal setting
* Setting type of operation from menu Account/Configuration/ISF/Bank transfer type 
""",
	'author': 'Matteo Angelino (matteo.angelino@informaticisenzafrontiere.org)',
	'website': 'www.informaticisenzafrontiere.org',
	'license': 'AGPL-3',
	'depends': ['account'],
	'data': ['wizard/isf_bank_transfer_view.xml'],
	'demo': [],
	'installable' : True,
}

