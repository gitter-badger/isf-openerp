# -*- encoding: utf-8 -*-

{
    'name': 'ISF COAA report',
    'version': '0.1',
    'depends': ['base', 'web', 'account_accountant', 'report_webkit'],
    'author': 'Antonio Verni(antonio.verni@informaticisenzafrontiere.org)',
    'description': """
ISF COAA Report
================================================

Add a report showing the full COAA 
    """,
    'license': 'AGPL-3',
    'category': 'Localization/Analytic Account Charts',
    'data': [
        'isf_coaa_report.xml',
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
