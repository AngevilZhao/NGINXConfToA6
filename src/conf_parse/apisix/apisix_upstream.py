from conf_parse.nginx.nginx_upstream import NGINXUpstream


class ApisixUpstream(object):
    def __init__(self, ngx_upstream: NGINXUpstream):
        self.ngx_upstream = ngx_upstream

        self.name = None
        self.nodes = []
        self.timeout = {
            "connect": 10,
            "read": 10,
            "send": 10
        }
        self.type = 'roundrobin'
        self.hash_on = None
        self.retries = 3

        self.checks = {}

    def parse(self):
        self.parse_name()
        self.parse_type()
        self.parse_nodes()

    def parse_name(self):
        self.name = self.ngx_upstream.ngx_upstream_name

    def parse_type(self):
        if self.ngx_upstream.ngx_ip_hash is True:
            self.type = "chash"
            self.hash_on = "$client_ip"
            return
        if self.ngx_upstream.hash is not None:
            self.type = "chash"
            self.hash_on = self.ngx_upstream.hash
            return

    def parse_nodes(self):
        for v in self.ngx_upstream.ngx_servers:
            self.nodes.append({
                "host:": v["host"],
                "weight": v["weight"],
                "priority": 10,
            })

    def to_dict(self):
        ret = {
            "name": self.name,
            "nodes": self.nodes,
            "timeout": self.timeout,
            "type": self.type,
            'retries': self.retries,
        }
        if self.hash_on is not None:
            ret["hash_on"] = self.hash_on
        return ret