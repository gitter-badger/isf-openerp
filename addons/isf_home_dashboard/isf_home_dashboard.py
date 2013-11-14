from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _
import time

class isf_home_dashboard_action_group(osv.osv):
    _name = "isf.home.dashboard.action.group"
    _description = "Group of home action"
    _columns = {
        'name': fields.char('Group name', size=100, required=True),
        'description': fields.char('Description', size=512),
        'sequence': fields.integer('Sequence', required=True, size=3),
    }

class isf_home_dashboard_action(osv.osv):
    """ Visible Dashboard Action """

    def route_to(self, cr, uid, ids, context=None):
        action_id = self.browse(cr, uid, ids[0], context)["action"] 
        aid = self.pool.get('ir.actions.actions').read(cr, uid, [action_id.id], fields=['id', 'type'], context=context)
        if not aid:
            raise Exception("Action configuration error: %s" % ids[0])
        next_action = self.pool.get(aid[0]['type']).read(cr, uid, [action_id.id], context=context)
        return next_action[0]

    _name = "isf.home.dashboard.action"
    _description = ""
    _columns = {
        'name' : fields.char('Visible name', size=100, required=True),
        'description': fields.char('Description', size=1024),
        'icon': fields.binary('icon'),
        'sequence': fields.integer('Sequence', required=True, size=3),
        'action': fields.many2one('ir.actions.actions', 'name'),
        'group': fields.many2one('isf.home.dashboard.action.group', 'group', required=True),
    }

isf_home_dashboard_action()

