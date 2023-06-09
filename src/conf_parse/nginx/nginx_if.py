from conf_parse.nginx import base
from conf_parse.nginx import nginx_const_vars as ngx_consts


class If(base.NGINXBlockBase):
    def __init__(self, ctx: base.Ctx, block: dict):
        super(If, self).__init__(ctx, block)
        self.left = None
        self.op = None
        self.right = None

        self.parse_not_total = True

        self.ins_ngx_return = None

    def parse(self):
        self.left = self.args[0]
        self.op = self.args[1]
        self.right = self.args[2]