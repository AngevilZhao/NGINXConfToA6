import queue
import json
import os

import crossplane
import yaml

from conf_parse.nginx import nginx_http
from conf_parse.nginx import base, nginx_location, nginx_server
from conf_parse.nginx import nginx_upstream


'''
if file is main nginx conf, crossplane will parse include files to blocks too
'''
class NGINXFileParser(object):
    def __init__(self, ctx, file_path):
        if ctx is None:
            dir_name = os.path.dirname(file_path)
            self.ctx = base.Ctx(dir_name)
        else:
            self.ctx = ctx
        self.ctx.ngx_file = file_path

        self.file_path = file_path
        self.wrap_file_path = self.file_path + ".wrap"
        self.block_parsed_error = None

        self.handler = None

    def convert(self):
        with open(self.file_path, "r") as f:
            file_content = f.read()
        wrap_content = "wrap {" + file_content + "}"
        with open(self.wrap_file_path, "w") as f:
            f.write(wrap_content)
        ori_blocks = crossplane.parse(self.wrap_file_path)
        print(json.dumps(ori_blocks))
        if len(ori_blocks["config"]) == 0:
            raise Exception(2, "config empty")
        self.ctx.ori_blocks = ori_blocks
        parsed = ori_blocks["config"][0]["parsed"][0]
        self.block_parsed_error = ori_blocks["config"][0]["errors"]
        # print("begin parse")
        self.convert_block(parsed)

    def convert_block(self, block: dict):
        self.handler = base.Wrap(self.ctx, block)
        self.handler.parse()

    def output(self):
        output_dict = {
            'file': self.file_path,
        }
        if self.block_parsed_error is not None:
            output_dict["block_parsed_error"] = self.block_parsed_error
        ret_map = self.search_by_bfs()
        for k, arr in ret_map.items():
            output_dict[k] = []
            for v in arr:
                output_dict[k].append(v.to_dict())
        return output_dict

    def search_by_bfs(self):
        ret_dict = {
            nginx_server.NGINXServer.__name__: [],
            nginx_upstream.NGINXUpstream.__name__: [],
            base.NotSupportBlock.__name__: [],
            base.NotImplBlock.__name__: [],
            "parse_exception_blocks": [],
            "parse_not_total_blocks": []
        }
        q = queue.Queue()
        q.put(self.handler)
        while True:
            if q.empty() is True:
                break
            handler = q.get()
            if len(handler.nginx_block_handlers) == 0:
                continue
            for k, block_handler_arr in handler.nginx_block_handlers.items():
                if len(block_handler_arr) == 0:
                    continue
                for bh in block_handler_arr:
                    q.put(bh)
                    class_name = bh.__class__.__name__
                    if class_name in ret_dict.keys():
                        ret_dict[class_name].append(bh)
                    if bh.parse_exception is not None:
                        ret_dict["parse_exception_blocks"].append(bh)
                    if bh.parse_not_total is True:
                        ret_dict["parse_not_total_blocks"].append(bh)
                    continue
        return ret_dict

    def match_upstream_for_router(self):
        pass


class NGINXDirParse(object):
    def __init__(self, dir_name):
        self.dir = dir_name

        self.ctx = base.Ctx(self.dir)

    def parse(self):
        main_conf = self.find_main_conf()
        file_parse = NGINXFileParser(self.ctx, main_conf)
        file_parse.convert()
        ret = file_parse.output()
        output_file = os.path.join(self.dir, "output.yaml")
        with open(output_file, 'a') as f:
            yaml.dump(ret, f)
        return ret

    def find_main_conf(self):
        main_conf_path = os.path.join(self.dir, "nginx.conf")
        return main_conf_path
