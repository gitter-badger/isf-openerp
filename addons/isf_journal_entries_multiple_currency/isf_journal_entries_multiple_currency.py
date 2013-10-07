import logging
from openerp.osv import fields, osv, orm

_logger = logging.getLogger(__name__)

class isfAccountVoucher(osv.Model):
	_description = 'ISF account.invoice'
	_inherit = 'account.voucher'
	
	def _get_company_currency(self, cr, uid, voucher_id, context=None):
		return self.pool.get('account.voucher').browse(cr,uid,voucher_id,context).journal_id.company_id.currency_id.id

	def _get_current_currency(self, cr, uid, voucher_id, context=None):
		voucher = self.pool.get('account.voucher').browse(cr,uid,voucher_id,context)
		return voucher.currency_id.id or self._get_company_currency(cr,uid,voucher.id,context)


	def _calculate_exchange(self, cr, uid, amount, currency, mult,context=None):
		other_currency = None
		currency_amount = 0.0
		currency_pool = self.pool.get('res.currency')
		currency_ids = currency_pool.search(cr, uid, [('active','=','1')], limit=2)
		currency_obj = currency_pool.browse(cr, uid, currency_ids, context=context)
		for cur in currency_obj:
			if cur.id != currency:
				 other_currency = cur
				 
		if other_currency:
			currency_amount = mult * amount * other_currency.rate
			
		return other_currency.id,currency_amount
	
		
		
	def proforma_voucher(self, cr, uid, ids, context=None):
		res = super(isfAccountVoucher, self).proforma_voucher(cr, uid, ids, context)	
		_logger.debug('MY proforma voucher')
		
		# Multiplier = 1 : debit, -1 : credit
		mult = 1
		
		if context is None:
			context = {}
			
		move_pool = self.pool.get('account.move')
		move_line_pool = self.pool.get('account.move.line')

		for voucher in self.browse(cr, uid, ids, context=context):
			if voucher.move_id:
				_logger.debug('Voucher.move_id : %d', voucher.move_id)
				
				company_currency = self._get_company_currency(cr, uid, voucher.id, context)
				current_currency = self._get_current_currency(cr, uid, voucher.id, context)
				
				if company_currency == current_currency:
					_logger.debug('I NEED TO CALCULATE OTHER CURRENCY')
					move_line_ids = move_line_pool.search(cr,uid,[('move_id','=', voucher.move_id.id)], context=context)
					move_lines = move_line_pool.browse(cr, uid, move_line_ids,context=context)
					for line in move_lines:
						_logger.debug('Move_line : name(%s) currency_id(%d) amount_currency(%f) debit(%f) credit(%f)',line.name, line.currency_id,line.amount_currency,line.debit,line.credit)
			
						mult = 1
						if line.credit > 0.0:
							mult = -1
							
						other_currency, amount_currency = self._calculate_exchange(cr, uid,voucher.amount,company_currency, mult, context=context)
						
						_logger.debug('Try to save : amount_currency = %d', amount_currency)
						
						move_line_pool.write(cr, uid, line.id, {'currency_id':other_currency,'amount_currency' : amount_currency})
					
					
		
		return res

		
isfAccountVoucher()

class isfAccountInvoice(osv.Model):
	_description = 'ISF account invoice'
	_inherit = 'account.invoice' 
	
	def _get_company_currency(self, cr, uid, invoice_id, context=None):
		return self.pool.get('account.invoice').browse(cr,uid,invoice_id,context).journal_id.company_id.currency_id.id

	def _get_current_currency(self, cr, uid, invoice_id, context=None):
		inv = self.pool.get('account.invoice').browse(cr,uid,invoice_id,context)
		return inv.currency_id.id or self._get_company_currency(cr,uid,inv.id,context)

	
	def _calculate_exchange(self, cr, uid, amount, currency, mult,context=None):
		other_currency = None
		currency_amount = 0.0
		currency_pool = self.pool.get('res.currency')
		currency_ids = currency_pool.search(cr, uid, [('active','=','1')], limit=2)
		currency_obj = currency_pool.browse(cr, uid, currency_ids, context=context)
		for cur in currency_obj:
			if cur.id != currency:
				 other_currency = cur
				 
		if other_currency:
			currency_amount = mult * amount * other_currency.rate
			
		return other_currency.id,currency_amount
	
	
	def action_move_create(self, cr, uid, ids, context=None):
		res = super(isfAccountInvoice,self).action_move_create(cr, uid, ids, context=context)
		
		move_obj = self.pool.get('account.move')
		move_line_pool = self.pool.get('account.move.line')
		
		if context is None:
			context = {}
		
		for inv in self.browse(cr,uid,ids,context=context):
			if inv.move_id:
				_logger.debug('Invoice[name(%s) move_id(%d)]', inv.name,inv.move_id)
				
				company_currency = self._get_company_currency(cr, uid, inv.id, context)
				current_currency = self._get_current_currency(cr, uid, inv.id, context)
				
				
				move_line_ids = move_line_pool.search(cr,uid, [('move_id','=', inv.move_id.id)], context=context)
				move_lines = move_line_pool.browse(cr, uid, move_line_ids, context=context)
		
				for line in move_lines:
					_logger.debug('Move line : name(%s)', line.name)
					
					mult = 1
					if line.credit > 0.0:
						mult = -1
							
					other_currency, amount_currency = self._calculate_exchange(cr, uid,inv.amount_total,company_currency, mult, context=context)
						
					_logger.debug('Try to save : amount_currency = %d', amount_currency)
						
					move_line_pool.write(cr, uid, line.id, {'currency_id':other_currency,'amount_currency' : amount_currency})
					
		
		return res
		
isfAccountInvoice()