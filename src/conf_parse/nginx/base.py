from traceback import format_exc
import os

from conf_parse.nginx import nginx_const_vars as ngx_consts


class Ctx(object):
    def __init__(self, ngx_conf_dir):
        self.ngx_dir = ngx_conf_dir
        self.ori_blocks = None
        self.globals = {}
        self.ngx_file = None


class NGINXBlockBase(object):
    def __init__(self, ctx: Ctx, block: dict):
        self.ctx = ctx
        self.block = block
        self.directive: str = self.block[ngx_consts.BlockConstDirective]
        self.line: int = self.block[ngx_consts.BlockConstLine]
        self.args: list = self.block[ngx_consts.BlockConstArgs]

        self.nginx_block_handlers = {}
        self.need_to_parse_directives = {}

        self.parent = None
        self.parse_exception = None
        self.parse_not_total = False

        # self.include_files_blocks = None

    def merge_parent_block(self, parent_block):
        parent_cls_name = self.parent.__class__.__name__
        if parent_cls_name == 'NGINXBlockBase':
            return

    def parse(self):
        from conf_parse.nginx.handers_map_def import NGINXBlockHandlerMap
        for directive in self.need_to_parse_directives:
            self.nginx_block_handlers[directive] = []
        if 'block' not in self.block:
            return
        for block in self.block['block']:
            block_handler = self.handle_block(block, NGINXBlockHandlerMap, self.ctx)
            '''
            handle include conf
            '''
        # if self.include_files_blocks is not None:
        #     # print("!!!!!", self.__class__.__name__)
        #     for file_info in self.include_files_blocks:
        #         ctx = Ctx(self.ctx.ngx_dir)
        #         ctx.globals = self.ctx.globals
        #         ctx.ngx_file = file_info['file']
        #         print(file_info)
        #         for parsed in file_info["parsed"]:
        #             self.handle_block(parsed, NGINXBlockHandlerMap, ctx)

    def parse_include(self, file_block):
        from conf_parse.nginx.handers_map_def import NGINXBlockHandlerMap
        # print("!!!!!", self.__class__.__name__)
        ctx = Ctx(self.ctx.ngx_dir)
        ctx.globals = self.ctx.globals
        ctx.ngx_file = file_block['file']
        print(file_block)
        for parsed in file_block["parsed"]:
            self.handle_block(parsed, NGINXBlockHandlerMap, ctx)

    def handle_block(self, block, NGINXBlockHandlerMap, ctx):
        directive = block[ngx_consts.BlockConstDirective]
        if directive not in self.need_to_parse_directives:
            block_handler = NotSupportBlock(self.ctx, block)
            self._append_block_handler(directive, block_handler)
            return block_handler
        if directive not in NGINXBlockHandlerMap and  'NGINXBlockHandlerMap' in self.__class__.__dict__ and \
                directive not in self.__class__.NGINXBlockHandlerMap:
            block_handler = NotImplBlock(self.ctx, block)
            self._append_block_handler(directive, block_handler)
            return block_handler
        if directive in self.__class__.NGINXBlockHandlerMap:
            cls = self.__class__.NGINXBlockHandlerMap[directive]
        else:
            cls = NGINXBlockHandlerMap[directive]
        # print("=====", directive, cls.__name__)
        if ctx is None:
            block_handler = cls(self.ctx, block)
        else:
            block_handler = cls(ctx, block)
        block_handler.parent = self
        self._append_block_handler(directive, block_handler)
        try:
            block_handler.parse()
        except Exception as e:
            print(format_exc())
            block_handler.parse_exception = e
        return block_handler

    def _append_block_handler(self, nginx_directive, block_handler):
        if nginx_directive in self.nginx_block_handlers:
            self.nginx_block_handlers[nginx_directive].append(block_handler)
        else:
            self.nginx_block_handlers[nginx_directive] = [block_handler]

    def to_dict(self):
        ret_dict = {
            ngx_consts.BlockConstDirective: self.directive,
            ngx_consts.BlockConstLine: self.line,
            "file": os.path.basename(self.ctx.ngx_file)
        }
        return ret_dict


class Wrap(NGINXBlockBase):
    NGINXBlockHandlerMap = {}

    def __init__(self, ctx, block: dict):
        super(Wrap, self).__init__(ctx, block)

        self.need_to_parse_directives = {
            ngx_consts.NGINXDirectiveHTTP: True,
            ngx_consts.NGINXDirectiveInclude: True,
        }

    def parse(self):
        super(Wrap, self).parse()


# this class means the nginx directive is decided not to be support to parse
class NotSupportBlock(NGINXBlockBase):
    def __init__(self, ctx, block: dict):
        super(NotSupportBlock, self).__init__(ctx, block)
        self.dump_yaml = True

    def to_dict(self):
        ret = super(NotSupportBlock, self).to_dict()
        return ret


# this class means the nginx directive is decided should to be support, but not has been implemented now
class NotImplBlock(NGINXBlockBase):
    def __init__(self, ctx, block: dict):
        super(NotImplBlock, self).__init__(ctx, block)
        self.dump_yaml = True

    def to_dict(self):
        ret = super(NotImplBlock, self).to_dict()
        return ret