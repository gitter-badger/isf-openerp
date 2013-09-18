{
    'name': 'Web',
    'category': 'Hidden',
    'version': '7.0.0.1',
    'description':
        """
OpenERP Web core module.
========================

This module provides an alternative login screen.
        """,
    'depends': ['web'],
    'qweb' : [
        "static/src/xml/web_userlist.xml",
    ],
    'css' : [
	"static/src/css/isf_base.css",
    ],
    'installable': True,
    'auto_install': True,
}
