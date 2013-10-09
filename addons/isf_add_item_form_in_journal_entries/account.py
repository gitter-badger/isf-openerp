from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _
import logging

_logger = logging.getLogger(__name__)
_debug = True

class account_move_line(osv.Model):
	_description = "ISF account move line"
	_inherit = "account.move.line"
	
	def _calculate_exchange(self, cr, uid, ids, currency_id, amount, context=None):
		currency_amount = 0.0
		currency_pool = self.pool.get('res.currency')
		currency_ids = currency_pool.search(cr, uid, [('id','=',currency_id)], limit=1)
		currency_obj = currency_pool.browse(cr, uid, currency_ids, context=context)
		
		for cur in currency_obj:
			if _debug:
				_logger.debug('RATE conversion %d : ',cur.rate)
			currency_amount = amount * cur.rate
			
		return currency_amount
		
	def onchange_debit(self, cr, uid, ids, debit, context=None):
		vals = {'value':{} }
		
		currency_id = context.get('currency_id',False)
		
		if _debug:
			_logger.debug('Debit : %d',debit)
			_logger.debug('Currency : %d', currency_id)
			
		amount_currency = self._calculate_exchange(cr, uid, ids, currency_id, debit, context=context)
		
		if debit > 0.0:
			vals['value'].update({
				'amount_currency' : amount_currency,
				'credit' : 0.0
			})
		
		return vals
		
	def onchange_credit(self, cr, uid, ids, credit, context=None):
		vals = {'value':{} }
		
		currency_id = context.get('currency_id',False)
		
		if _debug:
			_logger.debug('Credit : %d',credit)
			_logger.debug('Currency : %d', currency_id)
		
		amount_currency = self._calculate_exchange(cr, uid, ids, currency_id, credit, context=context)
		
		if credit > 0.0:
			vals['value'].update({
				'amount_currency' : amount_currency,
				'debit' : 0.0
			})
		
		return vals 
	
	
account_move_line()