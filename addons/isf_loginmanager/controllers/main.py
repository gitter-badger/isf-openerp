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
            #loginbox = registry['loginox.public']
            userModel = db_registry['res.users']
            cr = db_registry.db.cursor()
            res = userModel.search(cr, 1, [('active', '=', 'true')])
            res = userModel.read(cr, 1, res, ['login', 'display_name'])
            #res = loginbox.read(cr, 1, res, [])
            #cr.commit()
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
            #loginbox = registry['loginox.public']
            groupsModel = db_registry['res.groups']
            cr = db_registry.db.cursor()
            #res = groupsModel.search(cr, 1, [('name', '=', 'Visible')])
            #res = groupsModel.search(cr, 1, [('name', '=', 'Access Rights')])
            res = [1] # gruppo Access Rights
            userModel = db_registry['res.users']
            res = userModel.search(cr, 1, [('groups_id', 'not in', res)])
            res = userModel.read(cr, 1, res, []) #'login', 'display_name'])
            #cr.commit()
        except Exception, ex:
            _logger.exception('Failed to execute ISFLoginManager method %s ' %  ex)
            raise
        finally:
            cr.close()
        return res

"""
import openerp.netsvc as netsvc
class loginbox(netsvc.ExportService):
    def __init__(self, name="loginbox"):
        netsvc.ExportService.__init__(self, name)

    def exp_public(self, db_name):
        try:
            registry = openerp.modules.registry.RegistryManager.get(db_name)
            assert registry, 'Unknown database %s' % db_name
            #loginbox = registry['loginox.public']
            loginbox = registry['res.users']
            cr = registry.db.cursor()
            res = loginbox.search(cr, 1, [('active', '=', 'true')])
            _logger.debug(res)
            res = loginbox.read(cr, 1, res, ['login', 'display_name', 'id', 'group_ids'])
            #res = loginbox.read(cr, 1, res, [])
            _logger.debug("%s %s" % (res, type(res[0])))

            #cr.commit()
        except Exception:
            _logger.exception('Failed to execute LoginBox method %s with args %r.', method_name, method_args)
            raise
        finally:
            cr.close()
        return res

    def dispatch(self, method, params):
        allowed = False
        if method in ['private']:
            (db, uid, passwd ) = params[0:3]
            openerp.service.security.check(db, uid, passwd)
        elif method not in ['public']:
            raise KeyError("Method not found: %s." % method)
        fn = getattr(self, 'exp_'+method)
        return fn(*params)
loginbox()
"""

"""
import openerp.http as http
    def _auth(self, db):
        reg = openerp.modules.registry.RegistryManager.get(db)
        uid = openerp.netsvc.dispatch_rpc('common', 'authenticate', [db, "anonymous", "anonymous", None])
        return reg, uid

    @http.route('/loginbox/public', auth="none")
    def loader(self, **kwargs):
        print kw
        p = json.loads(kwargs["p"])
        db = p["db"]
        channel = p["channel"]
        user_name = p.get("user_name", None)

        reg, uid = self._auth(db)
        with reg.cursor() as cr:
            info = reg.get('im_livechat.channel').get_info_for_chat_src(cr, uid, channel)
            info["db"] = db
            info["channel"] = channel
            info["userName"] = user_name
            return request.make_response(env.get_template("loader.js").render(info),
                 headers=[('Content-Type', "text/javascript")])
"""


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
