# -*- coding: utf-8 -*-

{
	'name': 'ISF Stock Output',
	'version': '0.2',
	'category': 'Tools',
	'description': """

ISF Stock Output
============================

This feature is used to reduce the stock asset one time the drugs are sold."
""",
	'author': 'Antonio Verni (antonio.verni@informaticisenzafrontiere.org)',
	'website': 'www.informaticisenzafrontiere.org',
	'license': 'AGPL-3',
	'depends': ['account_accountant', 'isf_home_dashboard'],
	'data': [
        'wizard/isf_stock_output_view.xml',
        'data/account_data.xml', 
        'data/isf.home.dashboard.action.csv'
    ],
	'demo': [],
	'installable' : True,
}

