# -*- coding: utf-8 -*-
{
	'name': 'ISF Cims Water - Models',
	'version': '0.1',
	'category': 'Water',
	'description': """
Cims Water - Models
============================

Application models
""",
	'author': 'Antonio Verni (antonio.verni@informaticisenzafrontiere.org)',
	'website': 'www.informaticisenzafrontiere.org',
	'license': 'AGPL-3',
	'depends': ['sale', 'hr', 'isf_currency_slsh'],
	'data': [
        'isf_cw_models_sequence.xml',
        'isf_cw_models_view.xml'
    ],
	'installable' : True,
	'demo': [],
}
