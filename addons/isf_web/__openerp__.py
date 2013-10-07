{
    'name': 'Isf Web',
    'category': 'Hidden',
    'version': '0.0.1',
    'description':
        """
This module provides an alternative login screen.
        """,
    'depends': ['web'],
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
