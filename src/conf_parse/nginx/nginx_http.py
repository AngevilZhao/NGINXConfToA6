from conf_parse.nginx import base
from conf_parse.nginx import nginx_const_vars as ngx_consts


class NGINXHttp(base.NGINXBlockBase):
    NGINXBlockHandlerMap = {}
    CanCopyToServer = ["ins_ngx_ssl", "ins_ngx_ssl_client"]

    def __init__(self, ctx, block):
        super(NGINXHttp, self).__init__(ctx, block)
        self.need_to_parse_directives = {
            ngx_consts.NGINXDirectiveServer: True,
            ngx_consts.NGINXDirectiveProxyConnectTimeout: True,
            ngx_consts.NGINXDirectiveProxySendTimeout: True,
            ngx_consts.NGINXDirectiveProxyReadTimeout: True,
            ngx_consts.NGINXDirectiveInclude: True,
            ngx_consts.NGINXDirectiveUpstream: True,
            ngx_consts.NGINXDirectiveAddHeader: True,
            ngx_consts.NGINXDirectiveSSLCertificate: True,
            ngx_consts.NGINXDirectiveSSLCertificateKey: True,
        }

        #  format is : {"crt": [crt1, ...], "key": [key1, ... ]}
        self.ins_ngx_ssl = {}
        self.ins_ngx_ssl_client = None

    def parse(self):
        super(NGINXHttp, self).parse()

