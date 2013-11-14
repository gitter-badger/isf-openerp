# -*- coding: utf-8 -*-
import logging
import openerp
import openerp.addons.web.http as openerpweb

_logger = logging.getLogger(__name__)

class ISFLoginManagerController(openerpweb.Controller):
    _cp_path = "/isf/loginmanager"

    @openerpweb.jsonrequest
    def active(self, req, db_name =''):
        res = None
        try:
            db_registry = openerp.modules.registry.RegistryManager.get(db_name)
            assert db_registry, 'Unknown database %s' % db_name
            userModel = db_registry['res.users']
            cr = db_registry.db.cursor()
            res = userModel.search(cr, 1, [('active', '=', 'true')])
            res = userModel.read(cr, 1, res, ['login', 'display_name'])
        except Exception, ex:
            _logger.exception('Failed to execute ISFLoginManager method %s ' %  e)
            raise
        finally:
            cr.close()
        return res

    @openerpweb.jsonrequest
    def public(self, req, db_name =''):
        res = None
        try:
            db_registry = openerp.modules.registry.RegistryManager.get(db_name)
            assert db_registry, 'Unknown database %s' % db_name
            groupsModel = db_registry['res.groups']
            cr = db_registry.db.cursor()
            res = [1] # gruppo Access Rights
            userModel = db_registry['res.users']
            res = userModel.search(cr, 1, [('groups_id', 'not in', res)])
            res = userModel.read(cr, 1, res, ['login', 'display_name'])
        except Exception, ex:
            _logger.exception('Failed to execute ISFLoginManager method %s ' %  ex)
            raise
        finally:
            cr.close()
        return res


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
