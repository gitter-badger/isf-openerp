{
    'name': 'ISF Journal Entries Layout',
    'category': 'Tools',
    'version': '7.0.0.2',
    'description':
        """
OpenERP (Journal Entries Layout)
========================

This module provides a patch to css of journal entries with double currency.
        """,
    'depends': ['web'],
    'css' : [
	"static/src/css/isf_base.css",
    ],
    'installable': True,
    'auto_install': False,
}
