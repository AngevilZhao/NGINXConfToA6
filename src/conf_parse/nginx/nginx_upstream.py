from conf_parse.nginx import base
from conf_parse.nginx import nginx_const_vars as ngx_consts


class NGINXUpstreamServer(base.NGINXBlockBase):
    def __init__(self, ctx, block):
        super(NGINXUpstreamServer, self).__init__(ctx, block)

        self.instance = None
        self.kvs = {}
        self.weight = None
        self.parse_not_total = True

    def parse(self):
        self.instance = self.args[0]
        for v in self.args[1:]:
            k, v = v.split("=")
            self.kvs[k] = v
        # weight default value is 1
        self.weight = self.kvs.get("weight") or 1
        self.parent.ngx_servers.append({
            "host": self.instance,
            "weight": self.weight,
        })


class IPHash(base.NGINXBlockBase):
    def __init__(self, ctx, block):
        super(IPHash, self).__init__(ctx, block)

    def parse(self):
        self.parent.ngx_ip_hash = True


class Hash(base.NGINXBlockBase):
    def __init__(self, ctx, block):
        super(Hash, self).__init__(ctx, block)

    def parse(self):
        self.parent.ngx_hash = self.args[0]


class NGINXUpstream(base.NGINXBlockBase):
    NGINXBlockHandlerMap = {
        ngx_consts.NGINXDirectiveServer: NGINXUpstreamServer,
    }

    def __init__(self, ctx, block):
        super(NGINXUpstream, self).__init__(ctx, block)
        self.need_to_parse_directives = {
            ngx_consts.NGINXDirectiveServer: True,
            ngx_consts.NGINXDirectiveIPHash: True,
            ngx_consts.NGINXDirectiveHash: True,
        }

        self.ngx_upstream_name = None
        self.ngx_servers = []
        self.ngx_ip_hash = False
        self.hash = None

        self.apisix_upstream = None

    def parse(self):
        self.ngx_upstream_name = self.args[0]
        super(NGINXUpstream, self).parse()

        from conf_parse.apisix import apisix_upstream
        self.apisix_upstream = apisix_upstream.ApisixUpstream(self)
        self.apisix_upstream.parse()

    def to_dict(self):
        ret = super(NGINXUpstream, self).to_dict()
        val = {
            "ngx_upstream_name": self.ngx_upstream_name,
            "ngx_servers": self.ngx_servers
        }
        ret['value'] = val
        ret['apisix_upstream'] = self.apisix_upstream.to_dict()
        return ret
    
    def convert_to_lua(self):
        pass


