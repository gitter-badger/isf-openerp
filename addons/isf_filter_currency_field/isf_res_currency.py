import logging
from openerp.osv import fields, osv

_logger = logging.getLogger(__name__)

class isf_res_currency(osv.osv):
	_description = "ISF currency configurator"
	_name = "isf.res.currency"
	
	def _init_currency(self, cr, uid, ids=None, context=None):
		_logger.debug('INIT : DISABLE CURRENCY')	
		cr.execute(""" UPDATE res_currency set active=False where name not in ('USD','SLSH')""")
		return True
		
isf_res_currency()