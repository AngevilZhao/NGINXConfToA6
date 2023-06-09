BlockConstDirective = "directive"
BlockConstLine = "line"
BlockConstArgs = "args"

'''
HTTP
'''
NGINXDirectiveHTTP = "http"


'''
server
'''
NGINXDirectiveServer = "server"
NGINXDirectiveServerName = "server_name"

NGINXDirectiveSSLCertificate = "ssl_certificate"
NGINXDirectiveSSLCertificateKey = "ssl_certificate_key"
NGINXDirectiveSSLClientCertificate = "ssl_client_certificate"


'''
location
'''
NGINXDirectiveLocation = "location"
NGINXDirectiveProxyPass = "proxy_pass"


'''
upstream
'''
NGINXDirectiveUpstream = "upstream"
NGINXDirectiveIPHash = "ip_hash"
NGINXDirectiveHash = "hash"


'''
other which can appear in more than one block
'''
NGINXDirectiveProxySetHeader = "proxy_set_header"
NGINXDirectiveProxyConnectTimeout = "proxy_connect_timeout"
NGINXDirectiveProxySendTimeout = "proxy_send_timeout"
NGINXDirectiveProxyReadTimeout = "proxy_read_timeout"
NGINXDirectiveInclude = "include"
NGINXDirectiveAddHeader = "add_header"
NGINXDirectiveRewrite = "rewrite"
NGINXDirectiveSet = "set"
NGINXDirectiveReturn = "return"
NGINXDirectiveIf = "if"

NGINXDirectiveAllow = "allow"
NGINXDirectiveDeny = "deny"


NGINX_DEFAULT_VARS = {
    "$arg_name": True,
    "$arg_name": True,
    "$binary_remote_addr": True,
    "$body_bytes_sent": True,
    "$bytes_sent": True,
    "$connection": True,
    "$connection_requests": True,
    "$content_length": True,
    "$content_type": True,
    "$cookie_name": True,
    "$document_root": True,
    "$document_uri": True,
    "$host": True,
    "$hostname": True,
    "$http_name": True,
    "$https": True,
    "$is_args": True,
    "$limit_rate": True,
    "$msec": True,
    "$nginx_version": True,
    "$pid": True,
    "$pipe": True,
    "$proxy_protocol_addr": True,
    "$query_string": True,
    "$realpath_root": True,
    "$remote_addr": True,
    "$remote_port": True,
    "$remote_user": True,
    "$request": True,
    "$request_body": True,
    "$request_body_file": True,
    "$request_completion": True,
    "$request_filename": True,
    "$request_length": True,
    "$request_method": True,
    "$request_time": True,
    "$request_uri": True,
    "$scheme": True,
    "$sent_http_name": True,
    "$server_addr": True,
    "$server_name": True,
    "$server_port": True,
    "$server_protocol": True,
    "$status": True,
    "$tcpinfo_rtt": True,
    "$tcpinfo_rttvar": True,
    "$tcpinfo_snd_cwnd": True, 
    "$tcpinfo_rcv_space": True,
    "$time_iso8601": True,
    "$time_local": True,
    "$uri": True,
}
