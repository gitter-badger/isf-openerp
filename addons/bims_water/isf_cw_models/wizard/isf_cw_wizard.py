from openerp.osv import fields, osv
from tools.translate import _
import logging
import datetime

_logger = logging.getLogger(__name__)
_debug=True

class isf_stock_output_config(osv.Model):
    _name = 'isf.stock.output.config'
    
    _columns = {
        'name' : fields.char('Name',size=64, required=True),
        'journal_id' : fields.many2one('account.journal','Journal',required=True),
        'asset_account' : fields.many2many('account.account','isf_so_account_asset','name','id','Asset',required=True),
        'expense_account' : fields.many2many('account.account','isf_so_account_expense','name','id','Expense',required=True),
        'analytic_account' : fields.many2many('account.analytic.account','isf_so_account_analytic','name','id','Analytic',required=True),
    }
    
    _defaults = {
        'name' : _name,
    }
    
isf_stock_output_config()

class isf_stock_output(osv.osv_memory):
    _name = 'isf.stock.output'

    def _get_default_journal_id(self, cr, uid, context=None):
        context = context or {}
        config_pool = self.pool.get('isf.stock.output.config')
        config_ids = config_pool.search(cr, uid, [],limit=1)
        config_obj = config_pool.browse(cr, uid, config_ids, context=context)
        if len(config_obj):
            return config_obj[0].journal_id.id
        return None
    
    def _get_asset_accounts(self, cr, uid, context=None):
        context = context or {}
        config_pool = self.pool.get('isf.stock.output.config')
        config_ids = config_pool.search(cr, uid, [])
        config_obj = config_pool.browse(cr, uid, config_ids, context=context)
        return [(account.id, account.code + " " + account.name) for cfg in config_obj for account in cfg.asset_account ]
    
    def _get_expense_accounts(self, cr, uid, context=None):
        """reads configured expenses account list"""
        context = context or {}
        config_pool = self.pool.get('isf.stock.output.config')
        config_ids = config_pool.search(cr, uid, [])
        config_obj = config_pool.browse(cr, uid, config_ids, context=context)
        return [(account.id, account.code + " " + account.name) for cfg in config_obj for account in cfg.expense_account ]
        
    def _get_currency_amount(self, cr, uid, context=None):
        return 0

    def _get_analytic_accounts(self, cr, uid, context=None):
        """reads configured analytic account list"""
        context = context or {}
        config_pool = self.pool.get('isf.stock.output.config')
        config_ids = config_pool.search(cr, uid, [])
        config_obj = config_pool.browse(cr, uid, config_ids, context=context)
        return [(account.id, account.code + " " + account.name) for cfg in config_obj for account in cfg.analytic_account ]
    
    def _check_analytic_accounts_display(self, cr, uid, context=None):
        """check if at least one journal has been setup in config"""
        context = context or {}
        config_pool = self.pool.get('isf.stock.output.config')
        config_ids = config_pool.search(cr, uid, [])
        config_obj = config_pool.browse(cr, uid, config_ids, context=context)
        return config_obj and len(config_obj) and len(config_obj[0].analytic_account)
        
    def _get_company_currency_id(self, cr, uid, context=None):
        users = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        return users.company_id.currency_id.id
	
    def stock_output(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data = self.browse(cr, uid, ids, context=context)[0]
        journal_id = self._get_default_journal_id(cr, uid, context=context)
        move_line_pool = self.pool.get('account.move.line')		
        move_pool = self.pool.get('account.move')
        move = move_pool.account_move_prepare(cr, uid, journal_id, data.date, ref=data.ref, context=context)	
        if _debug:
            _logger.debug('Context : %s', context)
            _logger.debug('Amount_currency : %f', data.currency_amount)
            _logger.debug('account_move_prepare : %s', move)
        move_id = move_pool.create(cr, uid, move, context=context)
        if _debug:
            _logger.debug('move_id : %s', move_id)
        company_currency_id = self._get_company_currency_id(cr, uid, context=context)
        currency_id = False
        amount_currency = False
        amount_currency_credit = False
        amount_currency_debit = False
        amount = data.currency_amount
        data.company_amount = self._convert_amount(cr, uid, amount, company_currency_id, context)
        if data.currency.id != company_currency_id:
            if _debug:
                _logger.debug('Setting second currency value')
            amount = data.company_amount
            amount_currency_credit = -1 * data.currency_amount
            amount_currency_debit = data.currency_amount
            amount_currency = data.currency_amount
            currency_id = data.currency.id
				
        move_line = {
            #'analytic_account_id': data.analytic_account or False, 
            'tax_code_id': False, 
            'tax_amount': 0,
            'ref' : data.ref,
            'name': data.name or '/',
            'currency_id': currency_id,
            'credit': data.company_amount,
            'debit': 0.0,
            'date_maturity' : False,
            'amount_currency': amount_currency_credit,
            'partner_id': False,
            'move_id': move_id,
            'account_id': int(data.asset_account),
            'state' : 'valid'
        }
		
        if _debug:
            _logger.debug('move_line : %s',move_line)
		
        result = move_line_pool.create(cr, uid, move_line,context=context,check=False)
		
        if _debug:
            _logger.debug('Result : %s', result)
			
        move_line = {
            'analytic_account_id': data.analytic_account or False, 
            'tax_code_id': False, 
            'tax_amount': 0,
            'ref' : data.ref,
            'name': data.name or '/',
            'currency_id': currency_id,
            'credit': 0.0,
            'debit': data.company_amount,
            'date_maturity' : False,
            'amount_currency': amount_currency_debit,
            'partner_id': False,
            'move_id': move_id,
            'account_id': int(data.expense_account),
            'state' : 'valid'
        }
	
        result = move_line_pool.create(cr, uid, move_line,context=context,check=False)
        if _debug:
            _logger.debug('Result : %s', result)
		
        return {'type': 'ir.actions.act_window_close'}
            
    def onchange_amount(self, cr, uid, ids,  currency,currency_amount,context=None):
        context = context or {}
        company_amount = self._convert_amount(cr, uid, currency_amount, currency, context)
        return {'value':{
                'company_amount' : company_amount,
            } 
        }

    def _convert_amount(self, cr, uid, amount, from_currency, context):
        currency_pool = self.pool.get('res.currency')
        company_currency = self._get_company_currency_id(cr, uid, context=context)
        return currency_pool.compute(cr, uid, from_currency, company_currency, amount, context=context)
        
    def onchange_currency(self, cr, uid, ids, currency, context=None):
        return {'value':{
            'currency_amount' : 0.0,
            'company_amount' : 0.0,
            } 
        }
        
    _columns = {
        'journal_id' : fields.many2one('account.journal','Journal', required=True),
        'ref' : fields.char('Reference', size=64),
        'name' : fields.char('Name', size=64, required=True),
        'date' : fields.date('Date', required=True),
        'currency' : fields.many2one('res.currency', 'Currency', required=True),
        'currency_amount' : fields.float('Currency Amount',digits=(12,4)),
        'company_amount' : fields.float('Company Amount',digits=(12,4), readonly=True),
        'asset_account' : fields.selection(_get_asset_accounts,'Asset account', required=True),
        'expense_account' : fields.selection(_get_expense_accounts,'Expense account', required=True),
        'analytic_account' : fields.selection(_get_analytic_accounts,'Analytic account', required=True),
        'analytic_account_display' : fields.boolean('Analytic Account View'),
    }
    
    _defaults = {
        'journal_id' : _get_default_journal_id,
        'date' : fields.date.context_today,
        'analytic_account_display' : _check_analytic_accounts_display,
        #'currency_amount': _get_currency_amount
    }
         
    def _install_models(self, cr, uid, ids=None, context=None):
        self._install_journal(cr, uid, ids, context)
        #self._install_accounts(cr, uid, ids, context)
        #self._install_action(cr, uid, ids, context)

    def _install_journal(self, cr, uid, ids=None, context=None):
        if context is None:
            context = {}
        journal_pool = self.pool.get('account.journal')
        journal_ids = journal_pool.search(cr, uid, [('code','=','SOJ')])
        journal_obj = journal_pool.browse(cr, uid, journal_ids, context=context)
        if len(journal_obj):
            _logger.debug('Default journal found') 
        else:
            _logger.debug('Default journal not found : create')
            seq_pool = self.pool.get('ir.sequence')
            seq_ids = seq_pool.search(cr, uid, [('name','=','Stock Output Sequence')])
            seq_obj = seq_pool.browse(cr, uid, seq_ids)
            if len(seq_obj) == 0 or seq_obj[0] is None:
                sequence_id = seq_pool.create(cr,uid, {
                    'name' : 'Stock Output Sequence',
                    'prefix' : 'SO/%(year)s/',
                    'padding' : 4,
                    'implementation' : 'no_gap',
                }, context=context) 
            else:
                sequence_id = seq_obj[0].id
            analytic_journal_id = self._get_analytic_journal_by_name(cr, uid, 'General')
            journal_pool.create(cr, uid, {
                'name' : 'Stock Output Journal',
                'code' : 'SOJ',
                'type' : 'general',
                'sequence_id' : sequence_id,
                'analytic_journal_id': analytic_journal_id,
                'update_posted' : True,
            }, context=context)
        return True

    def _get_analytic_journal_by_name(self, cr, uid, name):
        analytic_account_pool = self.pool.get('account.analytic.journal')
        analytic_account_ids = analytic_account_pool.search(cr, uid, [('name','=',name)])
        return analytic_account_ids[0] if len(analytic_account_ids) else None

isf_stock_output()
