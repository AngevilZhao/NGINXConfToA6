from conf_parse.nginx import nginx_const_vars as consts
from conf_parse.nginx import nginx_http
from conf_parse.nginx import nginx_server
from conf_parse.nginx import nginx_location
from conf_parse.nginx import nginx_directive
from conf_parse.nginx import nginx_upstream
from conf_parse.nginx import nginx_if


NGINXBlockHandlerMap = {
    consts.NGINXDirectiveHTTP: nginx_http.NGINXHttp,

    consts.NGINXDirectiveServer: nginx_server.NGINXServer,
    consts.NGINXDirectiveServerName: nginx_server.ServerName,
    consts.NGINXDirectiveSSLCertificate: nginx_server.SSLCertificate,
    consts.NGINXDirectiveSSLCertificateKey: nginx_server.SSLCertificateKey,
    consts.NGINXDirectiveSSLClientCertificate: nginx_server.SSLClientCertificate,

    consts.NGINXDirectiveLocation: nginx_location.NGINXLocation,
    consts.NGINXDirectiveProxyPass: nginx_location.ProxyPass,

    consts.NGINXDirectiveUpstream: nginx_upstream.NGINXUpstream,
    consts.NGINXDirectiveIPHash: nginx_upstream.IPHash,
    consts.NGINXDirectiveHash: nginx_upstream.Hash,

    consts.NGINXDirectiveProxySetHeader: nginx_directive.ProxySetHeader,
    consts.NGINXDirectiveInclude: nginx_directive.Include,
    consts.NGINXDirectiveProxyConnectTimeout: nginx_directive.ProxyConnectTimeout,
    consts.NGINXDirectiveProxyReadTimeout: nginx_directive.ProxyReadTimeout,
    consts.NGINXDirectiveProxySendTimeout: nginx_directive.ProxySendTimeout,
    consts.NGINXDirectiveAddHeader: nginx_directive.AddHeader,
    consts.NGINXDirectiveRewrite: nginx_directive.Rewrite,
    consts.NGINXDirectiveSet: nginx_directive.Set,
    consts.NGINXDirectiveReturn: nginx_directive.Return,
    
    consts.NGINXDirectiveIf: nginx_if.If,
    consts.NGINXDirectiveAllow: nginx_directive.Allow,
    consts.NGINXDirectiveDeny: nginx_directive.Deny,
}
