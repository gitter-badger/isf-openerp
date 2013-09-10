# -*- coding: utf-8 -*-

{
	'name': 'Manage District',
	'version': '0.4',
	'category': 'Tools',
	'description': """
District management
===================

Adding new functionality to manage district, zone and sub zones. From the new menu
'Manage District' the user can:

* Define a new district or modify one
* Define a new zone to the district
* Define a sub zone for a couple (District, zone)
* Define a block for the tuple <District, zone, subzone>
* Define the plots for the blocks
""",
	'author': 'Matteo Angelino (matteo.angelino@informaticisenzafrontiere.org)',
	'website': 'www.informaticisenzafrontiere.org',
	'license': 'AGPL-3',
	'depends': ['product'],
	'data': ['isf_district_view.xml'],
	'demo': [],
	'installable' : True,
}

