{
    'name': 'Isf Login Manager',
    'category': 'Authentication',
    'version': '0.0.1',
    'description':
        """
This module provides an alternative login screen.
        """,
    'depends': ['base', 'web'],
    'data_xml': [
        #'security/ir.model.access.csv',
        'security/isf_userbox.xml',
    ],
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
    'auto_install': True,
    'bootstrap': True,
}
