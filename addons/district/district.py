from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _
import time

class district_district(osv.osv):
	""" District """
	_name = "district.district"
	_description = "District"
	_columns = {
		'code' : fields.char('District code', size=20, required=True),
		'name' : fields.char('District name', size=100, required=True),
	}
	
	_sql_constraints = [
        	('code', 'unique(code)', 'The code of the district must be unique')
    	]


district_district()

class district_zone(osv.osv):
	""" Zone """
	_name = "district.zone"
	_description = "Zone"
	_columns = {
		'code' : fields.char('Zone code', size=20, required=True),
		'district_ids' : fields.many2one('district.district', 'code'),
		'name' : fields.char('Zone name', size=100, required=True),
	}
	
	_sql_constraints = [
        	('code_zone_uniq', 'unique(code,district_ids)', 'The code of the district must be unique'),
    	]

	
district_zone()

class district_subzone(osv.osv):
	""" Sub Zone """
	_name = "district.subzone"
	_description = "Sub Zone"
	_columns = {
		'code' : fields.char('Sub Zone code', size=20, required=True),
		'zone_ids' : fields.many2one('district.zone', 'code'),
		'district_ids' : fields.many2one('district.district', 'code'),
		'name' : fields.char('Sub Zone name', size=100, required=True),
	}
	
	_sql_constraints = [
        	('code_subzone_uniq', 'unique(code,zone_ids,district_ids)', 'The code of the district must be unique'),
    	]

	
district_subzone()

class district_plot(osv.osv):
	""" Plot """
	_name = "district.plot"
	_description = "Plot"
	_columns = {
		'code' : fields.char('Plot Code', size=10, required=True),
		'subzone_ids' : fields.many2one('district.subzone',"code"),
		'zone_ids' : fields.many2one('district.zone', "code"),
		'district_ids' : fields.many2one('district.district', 'code'),
		'block' : fields.integer('Plot Number', size=4, required=True),
		'width' : fields.integer('Width',size=4, Required=False),
		'height' : fields.integer('Height',size=4, Required=False),
		'unit_ids' : fields.many2one('product.uom', 'Unit of Measure',required=False), 
	}
	
	_sql_constraints = [
        	('code_plot_uniq', 'unique(code,subzone_ids,zone_ids,district_ids)', 'The code of the plot must be unique')
    	]
	
district_plot()




