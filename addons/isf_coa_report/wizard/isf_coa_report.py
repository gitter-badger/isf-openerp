# -*- coding: utf-8 -*-
from openerp.osv import orm, fields, osv
from openerp import netsvc

class isf_hgh_coa_account(osv.osv_memory):
    _name = "isf.hgh.coa.account"
    _description = "COA Account"
    _columns = {
        'account': fields.many2one('account.account', "Account", select=True)
    }

isf_hgh_coa_account()
