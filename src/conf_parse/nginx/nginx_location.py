from copy import deepcopy
import re

from conf_parse.nginx import base
from conf_parse.nginx import nginx_const_vars as ngx_consts
from conf_parse.nginx import nginx_server
from conf_parse.nginx import nginx_directive


class NGINXLocation(base.NGINXBlockBase):
    NGINXBlockHandlerMap = {}

    def __init__(self, ctx, block):
        super(NGINXLocation, self).__init__(ctx, block)
        self.block_server = None

        self.need_to_parse_directives = {
            ngx_consts.NGINXDirectiveProxyPass: True,
            ngx_consts.NGINXDirectiveProxySetHeader: True,
            ngx_consts.NGINXDirectiveProxyConnectTimeout: True,
            ngx_consts.NGINXDirectiveProxySendTimeout: True,
            ngx_consts.NGINXDirectiveProxyReadTimeout: True,
            ngx_consts.NGINXDirectiveAddHeader: True,
            ngx_consts.NGINXDirectiveSet: True,
        }

        self.need_to_merge_block = {}

        self.ngx_hosts = None
        self.ngx_uri_op = None
        self.ngx_uri = []

        self.ngx_proxy_set_headers = {}
        self.ngx_add_headers = {}

        # 60 is the default value in nginx
        self.proxy_connect_timeout = 60
        self.proxy_send_timeout = 60
        self.proxy_read_timeout = 60

        self.proxy_pass_prefix_uri = None
        self.proxy_pass_upstream_format = None
        self.proxy_pass_upstream_name = None

        self.ngx_rewrite_info = []

        self.ngx_set_vars = {}

        self.ins_ngx_return: nginx_directive.Return = None

        self.ins_ngx_if_arr = None

        
        self.apisix_router = None

    def merge_parent_block(self, parent: nginx_server.NGINXServer):
        parent_cls_name = parent.__class__.__name__
        if parent_cls_name != 'NGINXServer':
            raise Exception("NGINXLocation merge_parent_block parent_cls_name:", parent_cls_name)
        for k in parent.__class__.CanCopyToLocation:
            self.__dict__[k] = deepcopy(parent.__dict__[k])

    def parse(self):
        self.merge_parent_block(self.parent)
        if len(self.args) == 1:
            if self.args[0][0] == "=":
                self.ngx_uri_op = "="
                self.ngx_uri = self.args[0][1:]
            else:
                self.ngx_uri = self.args[0]
        elif len(self.args) == 2:
            self.ngx_uri_op = self.args[0]
            self.ngx_uri = self.args[1]

        super(NGINXLocation, self).parse()

        from conf_parse.apisix import apisix_router
        self.apisix_router = apisix_router.ApisixRouter(self)
        self.apisix_router.parse()

        self.parent.ins_ngx_locations.append(self)

    def to_dict(self):
        ret = super(NGINXLocation, self).to_dict()
        val = {
            'ngx_url_op': self.ngx_uri_op,
            'ngx_url': self.ngx_uri,
            'proxy_timeout': {
                'connect': self.proxy_connect_timeout,
                'send': self.proxy_send_timeout,
                'read': self.proxy_read_timeout,
            }
        }
        if self.proxy_pass_upstream_format is not None:
            val['proxy_pass_upstream_format'] = self.proxy_pass_upstream_format
        if self.proxy_pass_upstream_name is not None:
            val['proxy_pass_upstream_name'] = self.proxy_pass_upstream_name
        ret['value'] = val
        ret['apisix_router'] = self.apisix_router.to_dict()
        return ret


class ProxyPass(base.NGINXBlockBase):
    def __init__(self, ctx, block):
        super(ProxyPass, self).__init__(ctx, block)

        self.https = False

        #  0: ip     1: DNS    2: upstream_name
        self.format = True

        self.prefix_uri = None

    def parse(self):
        val = ""
        if self.args[0].startswith("https:"):
            self.https = True
            val = self.args[0][len("https://"):-1]
        else:
            val = self.args[0][len("http://"):-1]
        elem_arr = val.split("/")
        # print("---------", elem_arr)
        if len(elem_arr) == 0:
            self.parse_exception = True
            return

        self.check_upstream_format(elem_arr[0])
        self.parent.proxy_pass_upstream_format = self.format
        self.parent.proxy_pass_upstream_name = elem_arr[0]

        self.check_prefix_uri(elem_arr, val)

    def check_prefix_uri(self, elem_arr, val: str):
        if len(elem_arr) == 1:
            if val[-1] == '/':
                return
            else:
                self.prefix_uri = self.parent.ngx_uri
                self.parent.proxy_pass_prefix_uri = self.prefix_uri
                return
        else:
            begin_pos = val.find("/")
            self.prefix_uri = val[begin_pos:]
            self.parent.proxy_pass_prefix_uri = self.prefix_uri
            return

    def check_upstream_format(self, s):
        elem_arr = s.split(":")
        valid = re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", elem_arr[0])
        if valid:
            self.format = 0
            return
        valid = re.match(r"^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]"
                         r"*[A-Za-z0-9])$", elem_arr[0])
        if valid:
            self.format = 1
            return
        self.format = 2



