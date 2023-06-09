from copy import deepcopy

from conf_parse.nginx.nginx_location import NGINXLocation


class ApisixPlugin(object):
    def __init__(self):
        self.plugin_name = None
        self.should_add_to_router = False

    def to_dict(self):
        return {}
    
    def parse(self):
        pass


class ProxyRewrite(ApisixPlugin):
    Name = "proxy-rewrite"

    def __init__(self, ngx_location: NGINXLocation):
        super(ProxyRewrite, self).__init__()

        self.scheme = None
        self.uri = None
        self.regex_uri = []
        self.host = None
        self.headers = {}
        self.add_headers = {}

        self.ngx_location = ngx_location

    def parse(self):
        self.parse_headers()
        self.parse_uri()

    def parse_headers(self):
        if self.ngx_location.ngx_proxy_set_headers is None:
            return
        for k, v in self.ngx_location.ngx_proxy_set_headers.items():
            val = v["value"]
            self.headers[k] = val
        self.should_add_to_router = True

    '''
    # $uri or $request_uri ?  
    '''
    def parse_uri(self):
        if self.ngx_location.proxy_pass_prefix_uri is not None:
            self.uri = self.ngx_location.proxy_pass_prefix_uri + "$uri"

    def parse_regex_uri(self):
        pass

    def __str__(self):
        return "class<ProxyRewrite>[ uri: {uri} ]".format(uri=self.uri)

    def to_dict(self):
        ret = {'disable': False}
        if self.uri is not None:
            ret['uri'] = self.uri
        if self.regex_uri is not None and len(self.regex_uri) > 0:
            ret['regex_uri'] = self.regex_uri
        if self.headers is not None:
            ret['headers'] = self.headers
        return ret


class Redirect(ApisixPlugin):
    Name = "redirect"

    def __init__(self, ngx_location: NGINXLocation):
        super(Redirect, self).__init__()
        self.ngx_location = ngx_location

        self.rewrites = []

        self.http_to_https: bool = None
        self.uri: str = None
        self.regex_uri = []
        self.ret_code: int = None
        self.encode_uri: bool = None
        self.append_query_string: bool = None

    def parse(self):
        if len(self.ngx_location.ngx_rewrite_info) == 0:
            return
        v = self.ngx_location.ngx_rewrite_info[0]
        self.regex_uri.append(v['re_uri'])
        self.regex_uri.append(v['redirect_uri'])
        self.ret_code = v['http_status']
        
        self.convert_ngx_return()

    def convert_ngx_return(self):
        if self.ngx_location.ins_ngx_return is None:
            return
        ins_return = self.ngx_location.ins_ngx_return
        if ins_return.return_mode == 2:
            self.uri = ins_return.return_val
            return

    def to_dict(self):
        ret = {'disable': False}
        if len(self.regex_uri) > 0:
            ret['regex_uri'] = self.regex_uri
        ret['ret_code'] = self.ret_code
        return ret


class ResponseRewrite(ApisixPlugin):
    Name = "response-rewrite"

    def __init__(self, ngx_location: NGINXLocation):
        super(ResponseRewrite, self).__init__()
        self.ngx_location = ngx_location

        self.status_code: int = None
        self.body: str = None
        self.body_base64: bool = None
        self.headers = {}
        self.vars = None

    def parse(self):
        self.parse_headers()

    def parse_headers(self):
        if self.ngx_location.ngx_add_headers is None:
            return
        for k, v in self.ngx_location.ngx_add_headers.items():
            val = v["value"]
            self.headers[k] = val
        self.should_add_to_router = True

    def to_dict(self):
        ret = {'disable': False}
        if self.status_code is not None:
            ret['status_code'] = self.status_code
        if self.body is not None:
            ret['body'] = self.body
        if self.body_base64 is not None:
            ret['body_base64'] = self.body_base64
        if len(self.headers) > 0:
            ret['headers'] = self.headers
        if self.vars is not None:
            ret['vars'] = self.vars
        return ret



class URIBlocker(ApisixPlugin):
    def __init__(self, ngx_location: NGINXLocation):
        super(URIBlocker, self).__init__()
        self.ngx_location = ngx_location

        self.block_rules = []
        self.rejected_code = None
        self.rejected_msg = None
        self.case_insensitive = False

    def parse(self):
        self.convert_ngx_return()

    def convert_ngx_return(self):
        if self.ngx_location.ins_ngx_return is None:
            return
        ins_return = self.ngx_location.ins_ngx_return
        if ins_return.return_mode == 0:
            self.block_rules.append(".*")
            self.rejected_code = ins_return.return_val
            return
        elif ins_return.return_mode == 1:
            self.block_rules.append(".*")
            self.rejected_code = 200
            self.rejected_msg = ins_return.return_val
            return
            

    def to_dict(self):
        ret = {}
        super(URIBlocker, self).to_dict()
        if len(self.block_rules) > 0:
            ret['block_rules'] = self.block_rules
        if self.rejected_code is not None:
            ret['rejected_code'] = self.rejected_code
        if self.rejected_msg is not None:
            ret['rejected_msg'] = self.rejected_msg
        ret['case_insensitive'] = self.case_insensitive

