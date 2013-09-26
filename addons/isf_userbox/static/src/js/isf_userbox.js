

openerp.isf_userbox = function(instance) {
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;

    instance.isf_userbox = {};

    instance.web.Login.include({
        start: function() {
            var self = this;
            return this._super().always(function(){
                var dbname = self.selected_db;
                //reader = new instance.isf_userbox.UserReader(dbname);
                //return reader.read().done(function(users){
                 
                instance.session.rpc("/isf/userbox/public", {'db_name': dbname})
                .done(function(users){
                    var select = $("select[name='userbox']");
                    $.each(users, function(idx, userData){
                        select.append($("<option></option>")
                            .attr("value", userData.login)
                            .text(userData.login + " - " + userData.display_name ))
                    });
                    select.change(function(){
                        var login = "";
                        $("select[name='userbox'] option:selected").each(function() {
                            login = $(this).val() ;
                        });
                        $("input[name='login']").val(login);
                    });
                });
            });
        },
    });
}

/*
    function makeErrorHandler(step){
        return function(){
            console.log(step + " error:", arguments);
        }
    }

    instance.isf_userbox.UserReader = instance.web.Class.extend(instance.web.EventDispatcherMixin, {
        init: function(db, username, password){
            instance.web.EventDispatcherMixin.init.call(this);
            this.db = db;
            this.username = username;
            this.password = password;
            //this.host = host || 'localhost';
            //this.port = port || 8069;
        },
        read: function(params) {
            var self = this;
            params = params || {};
            var publicCall = $.xmlrpc({
                url: '/xmlrpc/loginbox',
                methodName: 'public',
                params: [this.db], // ['hgh', 'admin', 'admin'],
            });
            var promise = $.when(publicCall, params.error || makeErrorHandler("loginbox.public"))
                        .pipe(function readUsers(response, status, jqXHR) { 
               return response[0][0]; 
            }, params.error || makeErrorHandler("read"));
            
            if(params.success){
                promise.done(params.success);
            }
            return promise;
        },
        // versione rpc 
        readRpc: function(params) {
            var self = this;
            params = params || {};

            var loginCall = $.xmlrpc({
                url: '/xmlrpc/common',
                methodName: 'login',
                params: [this.db, this.username, this.password], // ['hgh', 'admin', 'admin'],
            });
            var errorHandler = params.error;
            var uid;
            var promise = $.when(loginCall, params.error || makeErrorHandler("login"))
            .then(function searchIds(response, status, jqXHR) { 
                if(!response[0][0]) throw new Error("Login failed");
                console.log(response);
                self.uid = Number(response[0]);
                return $.xmlrpc({
                    url: '/xmlrpc/object',
                    methodName: 'execute',
                    params: [self.db, self.uid, self.password, 'res.users', 'search', []],
                });
            }, params.error || makeErrorHandler("search"))
            .then(function readUsers(response, status, jqXHR) { 
                return $.xmlrpc({
                    url: '/xmlrpc/object',
                    methodName: 'execute',
                        params: [self.db, self.uid, self.password, 'res.users', 'read', response[0]],
                    });
            }, params.error || makeErrorHandler("read"));
            if(params.success){
                promise.done(params.success);
            }
            return promise;
        },
    });
    */

