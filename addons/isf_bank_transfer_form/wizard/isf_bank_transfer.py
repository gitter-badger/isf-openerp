from openerp.osv import fields, osv
from tools.translate import _
import logging
import datetime

_logger = logging.getLogger(__name__)
_debug=True

class account_journal(osv.osv):
	_inherit = 'account.journal'
	
	_columns = {
		'bank_operations' : fields.boolean('Bank\Cash operations'),
	}
	
	_defaults = {
		'bank_operations' : False,
	}
	
account_journal()

class isf_bank_transfer_type(osv.Model):
	_name = 'isf.bank.transfer.type'
	
	_columns = {
		'name' : fields.char('Code',size=64, required=True),
		'description' : fields.char('Description', size=64, required=True),
		'type' : fields.selection((('0','bank-to-bank'),('1','bank-to-cash')), 'Type', required=True),
		'default' : fields.boolean('Default', required=False),
	}
	
isf_bank_transfer_type()

class isf_bank_transfer(osv.osv_memory):
	_name = 'isf.bank.transfer'


	_columns = {
		'name' : fields.many2one('isf.bank.transfer.type','Name', required=True),
		'date' : fields.date('Date',select=True,required=True),
		'amount' : fields.float('Amount',digits=(12,4),required=True),
		'currency' : fields.many2one('res.currency','Currency',required=True),
		'amount_currency' : fields.float('Amount currency', digits=(12,4)),
		'amount_company_currency' : fields.float('Amount company currency', digits=(12,4),required=True),
		'account_src' : fields.many2one('account.account','Source',required=True),
		'account_dst' : fields.many2one('account.account','Destination',required=True),
		# Hidden fields
		'journal_id' : fields.many2one('account.journal','Journal'),
		'period_id': fields.many2one('account.period', 'Period')
	}
	
	_defaults = {
		'date' : fields.date.context_today,
		'amount_currency' : 0.0,
	}
	
	def _get_company_currency_id(self, cr, uid, context=None):
		users = self.pool.get('res.users').browse(cr, uid, uid, context=context)
		company_id = users.company_id.id
		currency_id = users.company_id.currency_id
		
		return currency_id.id
			
	def make_transfer(self, cr, uid, ids, context=None):
		if context is None:
			context = {}
		data = self.browse(cr, uid, ids, context=context)[0]

		journal_id = self._get_default_journal_id(cr, uid, context=context)
		actual_period_id = self._get_actual_period_id(cr, uid, context=context)

		move_line_pool = self.pool.get('account.move.line')		
		move_pool = self.pool.get('account.move')
		
		move = move_pool.account_move_prepare(cr, uid, journal_id, data.date, context=context)	
	
		if _debug:
			_logger.debug('Context : %s', context)
			_logger.debug('Amount_currency : %f', data.amount_currency)
			_logger.debug('Amount currency (c) : %f', data.amount_company_currency)
			_logger.debug('account_move_prepare : %s', move)

		move_id = move_pool.create(cr, uid, move, context=context)
		
		if _debug:
			_logger.debug('move_id : %s', move_id)

		
		company_currency_id = self._get_company_currency_id(cr, uid, context=context)
		currency_id = False
		amount_currency = False
		amount_currency_credit = False
		amount = data.amount
		
		if _debug:
			_logger.debug('Company currency : %d , currency_id : %d', company_currency_id, data.currency)
		
		if data.currency.id != company_currency_id:
			if _debug:
				_logger.debug('Setting second currency value')
			amount = data.amount_company_currency
			amount_currency_credit = -1 * data.amount
			amount_currency = data.amount
			currency_id = data.currency.id
				
		move_line = {
			'analytic_account_id': False, 
			'tax_code_id': False, 
			'tax_amount': 0,
			'name': data.name.name or '/',
			'currency_id': currency_id,
			'credit': amount,
			'debit': 0.0,
			'date_maturity' : False,
			'amount_currency': amount_currency_credit,
			'partner_id': False,
			'move_id': move_id,
			'account_id': data.account_src.id
		}
		
		if _debug:
			_logger.debug('move_line : %s',move_line)
		
		result = move_line_pool.create(cr, uid, move_line,context=context,check=False)
		
		if _debug:
			_logger.debug('Result : %s', result)
			
		move_line = {
			'analytic_account_id': False, 
			'tax_code_id': False, 
			'tax_amount': 0,
			'name': data.name.name or '/',
			'currency_id': currency_id,
			'credit': 0.0,
			'debit': amount,
			'date_maturity' : False,
			'amount_currency': amount_currency,
			'partner_id': False,
			'move_id': move_id,
			'account_id': data.account_dst.id
		}
		
		result = move_line_pool.create(cr, uid, move_line,context=context,check=False)
		
		if _debug:
			_logger.debug('Result : %s', result)
		
	
		return {'type': 'ir.actions.act_window_close'}
		
	def _get_default_journal_id(self, cr, uid, context=None):
		if context is None:
			context = {}
		
		journal_pool = self.pool.get('account.journal')
		journal_ids = journal_pool.search(cr, uid, [('bank_operations','=',True)], limit=1)
		journal_obj = journal_pool.browse(cr, uid, journal_ids, context=context)
		
		for journal in journal_obj:
			return journal.id
	
	
	def _get_actual_period_id(self, cr, uid, context=None):
		if context is None:
			context = {}
			
		period_pool = self.pool.get('account.period')
		period_ids = period_pool.search(cr, uid, [])
		period_obj = period_pool.browse(cr, uid, period_ids, context=context)
		
		now = datetime.datetime.now()
		now_str = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
		
		period_id = None
		for period in period_obj:
			if _debug:
				if now_str <= period.date_stop and now_str >= period.date_start:
					period_id = period.id
					_logger.debug('Now : %s Start : %s , Stop : %s',now_str, period.date_start, period.date_stop)
				
		return period_id
		
	def onchange_amount(self, cr, uid, ids, currency, amount, context=None):
		result = {'value':{} }
		
		if context is None:
			context = {}
			
		if _debug:
			_logger.debug('onchange_amount : %s',context)
		
			
		account_dst_id = context.get('account_dst_id')
		journal_pool = self.pool.get('account.journal')
		journal_dst_ids = journal_pool.search(cr, uid, [('default_credit_account_id','=',account_dst_id)],limit=1)
		
		account_src_id = context.get('account_dst_id')
		journal_src_ids = journal_pool.search(cr, uid, [('default_credit_account_id','=',account_src_id)],limit=1)
		
		
		currency_id = context.get('currency_id')	
		currency_id_dst = None
		
		for j_src in journal_pool.browse(cr, uid, journal_src_ids):
			currency_id_src = j_src.currency.id
		
			
		for j_dst in journal_pool.browse(cr, uid, journal_dst_ids):
			currency_id_dst = j_dst.currency.id
		
		company_currency = self._get_company_currency_id(cr, uid, context=context)
		currency_dst = company_currency
		
		if company_currency != currency_id:
			currency_dst = currency_id
		elif company_currency != currency_id_src:
			currency_dst = currency_id_src
		elif company_currency != currency_id_dst:
			currency_dst = currency_id_dst
			
		if _debug:
			_logger.debug('Currency dst : %d',currency_dst)
		
		currency_pool = self.pool.get('res.currency')
		
		amount_currency = amount
		amount_currency = currency_pool.compute(cr, uid, currency_id, currency_dst,amount, context=context)
		amount_company_currency = currency_pool.compute(cr, uid, currency_id, company_currency, amount, context=context)
		result['value'].update({
			'amount_currency' : amount_currency,
			'amount_company_currency' : amount_company_currency,
		})
			
		return result
	
isf_bank_transfer()