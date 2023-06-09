from copy import deepcopy

from conf_parse.nginx import nginx_server


class ApisixSSL(object):
    def __init__(self, nginx_server: nginx_server.NGINXServer):
        self.nginx_server = nginx_server

        self.cert = None
        self.key = None
        self.certs = []
        self.keys = []

        # {"ca": xxx, "depth": xxx}
        self.client = None
        self.snis = []
        self.labels = None
        self.status = None

    def parse(self):
        if len(self.nginx_server.ins_ngx_ssl) == 0:
            return
        self.status = 1
        self.parse_cert()
        self.parse_key()
        self.parse_sni()
    
    def parse_cert(self):
        if "crt" not in self.nginx_server.ins_ngx_ssl:
            return
        if len(self.nginx_server.ins_ngx_ssl["crt"]) == 0:
            return
        self.cert = self.nginx_server.ins_ngx_ssl["crt"][0].crt
        for v in self.nginx_server.ins_ngx_ssl["crt"][1:]:
            self.certs.append(v.crt)

    def parse_key(self):
        if "key" not in self.nginx_server.ins_ngx_ssl:
            return
        if len(self.nginx_server.ins_ngx_ssl["key"]) == 0:
            return
        self.cert = self.nginx_server.ins_ngx_ssl["key"][0].key
        for v in self.nginx_server.ins_ngx_ssl["key"][1:]:
            self.certs.append(v.key)

    def parse_sni(self):
        if len(self.nginx_server.ngx_hosts) == 0:
            return
        self.snis = deepcopy(self.nginx_server.ngx_hosts["value"])

    def parse_client(self):
        if self.nginx_server.ins_ngx_ssl_client is None:
            return
        self.client = {}
        self.client["ca"] = self.nginx_server.ins_ngx_ssl_client.ca
        self.client["depth"] = 1

    def to_dict(self):
        ret = {}
        if self.cert is not None:
            ret["cert"] = self.cert
        if self.key is not None:
            ret["key"] = self.key
        if len(self.certs) > 0:
            ret["certs"] = self.certs
        if len(self.keys) > 0:
            ret["keys"] = self.keys
        if len(self.snis) > 0:
            ret["sni"] = self.snis
        if self.client is not None:
            ret["client"] = self.client
        ret["status"] = self.status
        return ret 