# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
from pprint import pprint as pp

from openerp.report import report_sxw

class isf_coaa_report_parser(report_sxw.rml_parse):
    _name = 'report.isf.coaa.webkit'

    def __init__(self, cr, uid, name, context=None):
        super(isf_coaa_report_parser, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'pp': pp,
            'lines': self.lines,
        })
        self.context = context
        self.result_acc = []

    def lines(self, ids=None, done=None):
        def _compute_tree(cr, uid, ids, field_names, context=None):
            account_obj = self.pool.get('account.analytic.account')
            recres = []
            def recursive_computation(account, res = None, level = 0):
                res = res or []
                res.append((account, level))
                for son in account.child_complete_ids:
                    recursive_computation(son, res, level + 1)
                return res
            for account in account_obj.browse(cr, uid, ids, context=context):
                recres.extend(recursive_computation(account))
            return recres

        ctx = self.context.copy()
        obj_account = self.pool.get('account.analytic.account')
        obj_report = self.pool.get('isf.hgh.coaa.account')
        report_data = obj_report.read(self.cr, self.uid, ctx['active_ids'], ['account'])
        if report_data[0]['account']:
            ids = [report_data[0]['account'][0]]
        else:
            ids = obj_account.search(self.cr, self.uid, [('parent_id', '=', False)])

        res = _compute_tree(self.cr, self.uid, ids, ['type','code','name','debit','credit','balance','parent_id','level','child_complete_ids'], ctx)
        pp(res)
        return res

report_sxw.report_sxw('report.isf.coaa.webkit', 'isf.hgh.coaa.account', 'addons/isf_coaa_report/report/coaa.mako', parser=isf_coaa_report_parser)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
