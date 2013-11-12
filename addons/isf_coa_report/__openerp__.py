# -*- encoding: utf-8 -*-

{
    'name': 'ISF COA report',
    'version': '0.1',
    'depends': ['base', 'web', 'account_accountant', 'report_webkit'],
    'author': 'Antonio Verni(antonio.verni@informaticisenzafrontiere.org)',
    'description': """
ISF COA Report
================================================

Add a report showing the full COA including empty accounts 
    """,
    'license': 'AGPL-3',
    'category': 'Localization/Account Charts',
    'data': [
        'wizard/isf_coa_report.xml',
    ],
    'demo': [],
    'qweb' : [
        "static/src/xml/*.xml",
    ],
    'css' : [
    	"static/src/css/*.css",
    ],
    'js' : [
    	"static/src/js/*.js",
    ],

    'installable': True,
    'auto_install': False,
}
