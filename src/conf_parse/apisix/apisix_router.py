from copy import deepcopy

from conf_parse.apisix import apisix_plugin
from conf_parse.nginx.nginx_location import NGINXLocation

a6_priority = {
    '=': 30,
    '^~': 10,
    '~': 5,
    '~*': 1,
}


class ApisixRouter(object):
    SupportLocPlugins = [
        apisix_plugin.ProxyRewrite,
        apisix_plugin.ResponseRewrite,
        apisix_plugin.Redirect,
    ]

    def __init__(self, ngx_location: NGINXLocation):
        self.ngx_location = ngx_location

        self.hosts = []
        self.uris = []
        self.priority = 0
        self.plugins = {}
        self.status = 1
        self.methods = ["GET", "HEAD", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
        self.timeout = {}

        self.support_plugins = {
            apisix_plugin.ProxyRewrite
        }

        # 0: ok  1: not ok  2: ignore
        self.valid_flag = 0
        self.invalid_reasons = []

    def to_dict(self):
        ret = {
            'hosts': self.hosts,
            'uris': self.uris,
            'priority': self.priority,
            'plugins': {},
            'status': 1,
            'methods': self.methods,
        }
        if len(self.timeout) > 0:
            ret['timeout'] = self.timeout
        for k, plugin in self.plugins.items():
            ret['plugins'][k] = plugin.to_dict()
        return ret

    def parse(self):
        self.parse_hosts()
        self.convert_url()
        self.parse_timeout()
        self.convert_priority()
        self.parse_plugins()

    def parse_hosts(self):
        value = self.ngx_location.ngx_hosts["value"]
        self.hosts = value

    def parse_timeout(self):
        self.timeout["connect"] = self.ngx_location.proxy_connect_timeout
        self.timeout["read"] = self.ngx_location.proxy_read_timeout
        self.timeout["send"] = self.ngx_location.proxy_send_timeout

    def parse_plugins(self):
        for plugin_cls in self.SupportLocPlugins:
            # print(plugin_cls.__name__, plugin_cls.Name)
            plugin_ins = plugin_cls(self.ngx_location)
            plugin_ins.parse()
            if plugin_ins.should_add_to_router:
                self.plugins[plugin_cls.Name] = plugin_ins

    '''
    * no op  -->  20
    * op =   -->  30
    * op ^~  -->  10
    * op ~   -->  5
    * op ~*  -->  1
    * @      -->  use for redirect, not support, do nothing
    '''
    def convert_url(self):
        if self.ngx_location.ngx_uri is None:
            self.valid_flag = 1
            self.invalid_reasons.append("judge_url error")
            return Exception("judge_url error")
        if self.ngx_location.ngx_uri_op is None:
            self.uris.append(self.ngx_location.ngx_uri + "*")
            return
        if self.ngx_location.ngx_uri_op == "=":
            self.uris.append(self.ngx_location.ngx_uri)
        else:
            self.uris.append("/*")

    '''
    * no op  -->  prefix match
    * op =   -->  exact match
    * op ^~  -->  not support, just convert to /*
    * op ~   -->  not support, just convert to /*
    * op ~*  -->  not support, just convert to /*
    * @      -->  use for redirect, not support, do nothing
    '''
    def convert_priority(self) -> Exception:
        if self.ngx_location.ngx_uri_op is None:
            self.priority = 20
            return
        self.priority = a6_priority[self.ngx_location.ngx_uri_op]
