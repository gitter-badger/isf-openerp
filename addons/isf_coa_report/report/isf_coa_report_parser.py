# -*- coding: utf-8 -*-
import time
from pprint import pprint as pp

from openerp.report import report_sxw

class isf_coa_report_parser(report_sxw.rml_parse):
    _name = 'report.isf.coa.webkit'

    def __init__(self, cr, uid, name, context=None):
        super(isf_coa_report_parser, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'pp': pp,
            'lines': self.lines,
        })
        self.context = context
        self.result_acc = []

    """"
    def set_context(self, objects, data, ids, report_type=None):
        for obj in objects:
            print obj, obj.id
        new_ids = ids
        return super(isf_coa_report_parser, self).set_context(objects, data, new_ids, report_type=report_type)
    """
    #def _add_header(self, node, header=1):
    #    if header == 0:
    #        self.rml_header = ""
    #    return True

    def lines(self, ids=None, done=None):
        def _process_child(accounts, disp_acc, parent):
            account_rec = [acct for acct in accounts if acct['id']==parent][0]
            currency_obj = self.pool.get('res.currency')
            acc_id = self.pool.get('account.account').browse(self.cr, self.uid, account_rec['id'])
            currency = acc_id.currency_id and acc_id.currency_id or acc_id.company_id.currency_id
            res = {
                'id': account_rec['id'],
                'type': account_rec['user_type'][1],
                'code': account_rec['code'],
                'name': account_rec['name'],
                'currency_id': currency_obj.read(self.cr, self.uid, [currency.id], ['name'])[0],
                'level': account_rec['level'],
                'balance': account_rec['balance'],
                'parent_id': account_rec['parent_id'],
                'bal_type': '',
            }
            if disp_acc == 'movement':
                #if not currency_obj.is_zero(self.cr, self.uid, currency, res['credit']) or not currency_obj.is_zero(self.cr, self.uid, currency, res['debit']) or not currency_obj.is_zero(self.cr, self.uid, currency, res['balance']):
                    self.result_acc.append(res)
            elif disp_acc == 'not_zero':
                #if not currency_obj.is_zero(self.cr, self.uid, currency, res['balance']):
                    self.result_acc.append(res)
            else:
                self.result_acc.append(res)
            if account_rec['child_id']:
                for child in account_rec['child_id']:
                    _process_child(accounts,disp_acc,child)

        obj_account = self.pool.get('account.account')
        ctx = self.context.copy()
        obj_report = self.pool.get('isf.hgh.coa.account')
        report_data = obj_report.read(self.cr, self.uid, ctx['active_ids'], ['account'])
        if report_data[0]['account']:
            ids = [report_data[0]['account'][0]]
        else:
            #res = obj_account.search(self.cr, self.uid, [('parent_id', '=', False)])
            #base_accounts = obj_account.read(self.cr, self.uid, res)
            #ids = [ data[0]['account'][0] for data in base_accounts ] 
            ids = obj_account.search(self.cr, self.uid, [('parent_id', '=', False)])

        if not ids:
            ids = self.ids
        if not ids:
            return []
        if not done:
            done={}

        """
        ctx['fiscalyear'] = form['fiscalyear_id']
        if form['filter'] == 'filter_period':
            ctx['period_from'] = form['period_from']
            ctx['period_to'] = form['period_to']
        elif form['filter'] == 'filter_date':
            ctx['date_from'] = form['date_from']
            ctx['date_to'] =  form['date_to']
        ctx['state'] = form['target_move']
        """

        parents = ids
        child_ids = obj_account._get_children_and_consol(self.cr, self.uid, ids, ctx)
        if child_ids:
            ids = child_ids
        accounts = obj_account.read(self.cr, self.uid, ids, ['user_type','code','name','debit','credit','balance','parent_id','level','child_id', 'currency_id', 'company_currency_id'], ctx)

        for parent in parents:
            if parent in done:
                continue
            done[parent] = 1
            _process_child(accounts,'all',parent)
        return self.result_acc

report_sxw.report_sxw('report.isf.coa.webkit', 'isf.hgh.coa.account', 'addons/isf_coa_report/report/coa.mako', parser=isf_coa_report_parser)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
