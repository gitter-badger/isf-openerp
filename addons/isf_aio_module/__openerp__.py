# -*- coding: utf-8 -*-

{
	'name': 'ISF All in one module',
	'version': '0.1',
	'category': 'Tools',
	'description': """
ISF All in one module installer
===============================
Install the following modules:

* ISF Currency SLSH
* ISF Hargeisa chart of accounts
* ISF Filter currency field
* ISF Journal entries layout
* ISF journal entries multiple currency
* ISF Payment method list in payments
* ISF login manager
* many2one enhanced
* pdf preview
""",
	'author': 'Matteo Angelino (matteo.angelino@informaticisenzafrontiere.org)',
	'website': 'www.informaticisenzafrontiere.org',
	'license': 'AGPL-3',
	'depends': [
		'isf_currency_slsh',
		#'isf_hgh_coa',
		'isf_filter_currency_field',
		'isf_journal_entries_layout',
		'isf_journal_entries_multiple_currency',
		'isf_payments_lists_filtering',
		'isf_loginmanager',
		'web_m2o_enhanced',
		'web_pdf_preview'
	],

	'data': [],
	'demo': [],
	'installable' : True,
}

