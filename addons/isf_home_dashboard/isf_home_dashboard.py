from openerp.osv import osv, orm
from openerp.osv import fields
from openerp.tools.translate import _
import time
import logging
import tools

_logger = logging.getLogger("isf_home_dashboard")

class isf_home_dashboard_action_group(osv.osv):
    _name = "isf.home.dashboard.action.group"
    _description = "ISF Home Dashboard Action Groups"
    _order = "sequence asc"
    _columns = {
        'name': fields.char('Group name', size=100, required=True),
        'description': fields.char('Description', size=512),
        'sequence': fields.integer('Sequence', required=True, size=3),
        'actions': fields.one2many('isf.home.dashboard.action', 'group', 'Actions'),
    }

class isf_home_dashboard_action(osv.osv):
    """ Visible Dashboard Action """

    @tools.cache()
    def allowed_actions(self, cr, uid, context=None):
        _logger.debug("isf_home_dashboard_action::allowed_actions")
        hdaction_ids = self.search(cr, uid, [], context=context)
        hdaction_data = self.read(cr, uid, hdaction_ids, fields=[], context=context)
        hdaction_data_dict = dict([(a['action'][0], a) for a in hdaction_data])
        actions = self.pool.get('ir.actions.actions')
        action_data = actions.read(cr, uid, [hda['action'][0] for hda in hdaction_data], context=context)
        visible_actions = []
        for a in action_data:
            model = self.pool.get(a['type'])
            try:
                real_action = model.read(cr, uid, a['id'], context=context)
                res_model = self.pool.get(real_action['res_model'])
                perm = res_model.check_access_rights(cr, uid, "read", raise_exception=False)
                if perm:
                    visible_actions.append(hdaction_data_dict[a['id']])
            except (orm.except_orm, ValueError, osv.except_osv), ex:
                # non authorized
                _logger.debug("Access not authorized to %s" % a['name'])
                _logger.debug(ex)
        return visible_actions

    def route_to(self, cr, uid, ids, context=None):
        action_id = self.browse(cr, uid, ids[0], context)["action"] 
        if not action_id:
            raise Exception("Action configuration error: %s" % ids)
        aid = self.pool.get('ir.actions.actions').read(cr, uid, [action_id.id], fields=['id', 'type'], context=context)
        if not aid:
            raise Exception("Action configuration error: %s" % ids[0])
        next_action = self.pool.get(aid[0]['type']).read(cr, uid, [action_id.id], context=context)
        return next_action[0]

    _name = "isf.home.dashboard.action"
    _columns = {
        'name' : fields.char('Visible name', size=100, required=True),
        'description': fields.char('Description', size=1024),
        'icon': fields.binary('Icon'),
        'sequence': fields.integer('Sequence', required=True, size=3),
        'action': fields.many2one('ir.actions.actions', 'Name', ondelete="cascade", select=True),
        'group': fields.many2one('isf.home.dashboard.action.group', 'Group', required=True),
        'groupsequence': fields.related('group', 'sequence'),
    }
    _description = "ISF Home Dashboard"
    _order = "sequence asc"

