from copy import deepcopy
import os

from conf_parse.nginx import base
from conf_parse.nginx import nginx_const_vars as ngx_consts
from conf_parse.utils import common_fun


class ProxySetHeader(base.NGINXBlockBase):
    def __init__(self, ctx, block: dict):
        super(ProxySetHeader, self).__init__(ctx, block)
        self.header = []

    def parse(self):
        self.header = self.args
        if self.args[0] == "A-Test":
            parent_cls_name = self.parent.__class__.__name__
            print("[debug]ProxySetHeader: ", parent_cls_name)
        self.parent.ngx_proxy_set_headers[self.header[0].lower()] = {
            "value": deepcopy(self.header[1]),
            "line": self.line,
        }


class Rewrite(base.NGINXBlockBase):
    def __init__(self, ctx, block: dict):
        super(Rewrite, self).__init__(ctx, block)

        self.re_uri = None
        self.redirect_uri = None
        self.flag = None
        self.http_status = None

    def parse(self):
        self.re_uri = self.args[0]
        self.redirect_uri = self.args[1]
        self.flag = self.args[2]
        if self.flag == "redirect":
            self.http_status = 302
        elif self.flag == "permanent":
            self.http_status = 301
        else:
            self.parse_not_total = True
        self.parent.ngx_rewrite_info.append({
            're_uri': self.re_uri,
            'redirect_uri': self.redirect_uri,
            'http_status': self.http_status,
        })


class Include(base.NGINXBlockBase):
    def __init__(self, ctx: base.Ctx, block: dict):
        super(Include, self).__init__(ctx, block)

        self.includes = block["includes"]
        # self.file_blocks = []

    def parse(self):
        # print("[Include] parent: ", self.parent.__class__.__name__)
        for v in self.includes:
            file_block = self.ctx.ori_blocks["config"][v]
            self.parent.parse_include(file_block)
        # self.parent.include_files_blocks = self.file_blocks


class ProxyConnectTimeout(base.NGINXBlockBase):
    def __init__(self, ctx: base.Ctx, block: dict):
        super(ProxyConnectTimeout, self).__init__(ctx, block)
        self.time = None

    def parse(self):
        self.time = self.args[0]
        self.parent.proxy_connect_timeout = self.args[0][0:-1]


class ProxySendTimeout(base.NGINXBlockBase):
    def __init__(self, ctx: base.Ctx, block: dict):
        super(ProxySendTimeout, self).__init__(ctx, block)
        self.time = None

    def parse(self):
        self.time = self.args[0]
        self.parent.proxy_send_timeout = self.args[0][0:-1]


class ProxyReadTimeout(base.NGINXBlockBase):
    def __init__(self, ctx: base.Ctx, block: dict):
        super(ProxyReadTimeout, self).__init__(ctx, block)
        self.time = None

    def parse(self):
        self.time = self.args[0]
        self.parent.proxy_read_timeout = self.args[0][0:-1]


class AddHeader(base.NGINXBlockBase):
    def __init__(self, ctx: base.Ctx, block: dict):
        super(AddHeader, self).__init__(ctx, block)
        self.header = {}

    def parse(self):
        self.header = self.args
        self.parent.ngx_add_headers[self.header[0].lower()] = {
            "value": deepcopy(self.header[1]),
            "line": self.line,
        }


class Set(base.NGINXBlockBase):
    def __init__(self, ctx: base.Ctx, block: dict):
        super(Set, self).__init__(ctx, block)
        self.key = None
        self.value = None

    def parse(self):
        self.key = self.args[0]
        self.value = self.args[1]
        self.parent.ngx_set_vars[self.key] = self.value


class Return(base.NGINXBlockBase):
    def __init__(self, ctx: base.Ctx, block: dict):
        super(Return, self).__init__(ctx, block)
        self.return_val: str = None
        # 0: code ;  1: text;   2: code
        self.return_mode = 0

    def parse(self):
        self.return_val = self.args[0]
        if self.is_code():
            self.return_mode = 0
        elif self.is_url:
            self.return_mode = 2
        else:
            self.return_mode = 1
        self.parent.ngx_return = self

    def is_code(self):
        return self.return_val.isnumeric()

    def is_url(self):
        return common_fun.check_str_is_url(self.return_val)


class Allow(base.NGINXBlockBase):
    def __init__(self, ctx: base.Ctx, block: dict):
        super(Allow, self).__init__(ctx, block)

        self.ip_format = None

    def parse(self):
        self.ip_format = self.args[0]
        if self.ip_format == "all":
            pass


class Deny(Allow):
    def __init__(self, ctx: base.Ctx, block: dict):
        super(Deny, self).__init__(ctx, block)
    




