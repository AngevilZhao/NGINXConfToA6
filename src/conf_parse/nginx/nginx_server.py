from copy import deepcopy
import os

from conf_parse.nginx import base
from conf_parse.nginx import nginx_http
from conf_parse.nginx import nginx_const_vars as ngx_consts


class ServerName(base.NGINXBlockBase):
    def __init__(self, ctx, block):
        super(ServerName, self).__init__(ctx, block)
        self.hosts = []

    def parse(self):
        self.hosts = deepcopy(self.args)
        # print(self.hosts)
        self.parent.ngx_hosts = {
            "value": self.hosts,
            "line": self.line,
        }


class SSLCertificate(base.NGINXBlockBase):
    def __init__(self, ctx, block):
        super(SSLCertificate, self).__init__(ctx, block)

        self.file_path = None
        self.ssl_crt = None

    def parse(self):
        self.file_path = self.args[0]
        file_path = os.path.join(self.ctx.ngx_dir, self.file_path)
        from conf_parse.utils import ssl
        self.ssl_crt = ssl.SSLCrt(file_path)
        self.ssl_crt.parse()
        # print("---------", self.ssl_crt.__dict__)

        if "crt" not in self.parent.ins_ngx_ssl:
            self.parent.ins_ngx_ssl["crt"] = [self.ssl_crt]
        else:
            self.parent.ins_ngx_ssl["crt"].append(self.ssl_crt)


class SSLClientCertificate(base.NGINXBlockBase):
    def __init__(self, ctx, block):
        super(SSLClientCertificate, self).__init__(ctx, block)

        self.file_path = None
        self.ca = None
    
    def parse(self):
        self.file_path = self.args[0]
        file_path = os.path.join(self.ctx.ngx_dir, self.file_path)
        with open(file_path, "r") as f:
            self.ca = f.read()
        


class SSLCertificateKey(base.NGINXBlockBase):
    def __init__(self, ctx, block):
        super(SSLCertificateKey, self).__init__(ctx, block)

        self.file_path = None
        self.ssl_key = None

    def parse(self):
        self.file_path = self.args[0]
        file_path = os.path.join(self.ctx.ngx_dir, self.file_path)
        from conf_parse.utils import ssl
        self.ssl_key = ssl.SSLKey(file_path)
        self.ssl_key.parse()

        if "key" not in self.parent.ins_ngx_ssl:
            self.parent.ins_ngx_ssl["key"] = [self.ssl_key]
        else:
            self.parent.ins_ngx_ssl["key"].append(self.ssl_key)


class NGINXServer(base.NGINXBlockBase):
    NGINXBlockHandlerMap = {}

    CanCopyToLocation = ["ngx_hosts", "ngx_proxy_set_headers", "ngx_add_headers",
                         "proxy_connect_timeout", "proxy_send_timeout", "proxy_read_timeout",
                         "ngx_set_vars"]

    def __init__(self, ctx, block):
        super(NGINXServer, self).__init__(ctx, block)
        self.block_http = None

        self.need_to_parse_directives = {
            ngx_consts.NGINXDirectiveServerName: True,
            ngx_consts.NGINXDirectiveLocation: True,
            ngx_consts.NGINXDirectiveProxySetHeader: True,
            ngx_consts.NGINXDirectiveProxyConnectTimeout: True,
            ngx_consts.NGINXDirectiveProxySendTimeout: True,
            ngx_consts.NGINXDirectiveProxyReadTimeout: True,
            ngx_consts.NGINXDirectiveInclude: True,
            ngx_consts.NGINXDirectiveAddHeader: True,
            ngx_consts.NGINXDirectiveSet: True,
            ngx_consts.NGINXDirectiveSSLCertificate: True,
            ngx_consts.NGINXDirectiveSSLCertificateKey: True,
        }

        self.need_to_merge_block = {}

        self.ngx_hosts = {}
        self.ngx_proxy_set_headers = {}
        self.ngx_add_headers = {}

        self.proxy_connect_timeout = None
        self.proxy_send_timeout = None
        self.proxy_read_timeout = None

        self.ngx_rewrite_info = []

        self.ngx_set_vars = {}

        self.ins_ngx_return = None

        #  format is : {"crt": [crt1, ...], "key": [key1, ... ]}
        self.ins_ngx_ssl = {}
        self.ins_ngx_ssl_client = None

        self.ins_ngx_locations = []


        self.apisix_ssl = None

    def merge_parent_block(self, parent: nginx_http.NGINXHttp):
        parent_cls_name = parent.__class__.__name__
        if parent_cls_name == 'NGINXHttp':
            return
        for k in parent.__class__.CanCopyToServer:
            self.__dict__[k] = deepcopy(parent.__dict__[k])

    def parse(self):
        super(NGINXServer, self).parse()
        from conf_parse.apisix import apisix_ssl
        if len(self.ins_ngx_ssl) > 0:
            self.apisix_ssl = apisix_ssl.ApisixSSL(self)
            self.apisix_ssl.parse()

    def to_dict(self):
        ret = super(NGINXServer, self).to_dict()
        val = {
            "ngx_hosts": self.ngx_hosts,
        }
        val["ngx_locations"] = []
        if len(self.ins_ngx_locations) > 0:
            for loc in self.ins_ngx_locations:
                val["ngx_locations"].append(loc.to_dict())
        if self.apisix_ssl is not None:
            val["apisix_ssl"] = self.apisix_ssl.to_dict()
        ret["value"] = val 
        return ret
