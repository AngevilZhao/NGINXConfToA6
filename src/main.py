import sys
import os
import argparse

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from conf_parse import parse
import http_server

parser = argparse.ArgumentParser()
parser.add_argument("-action", help="tool or http_server", type=str)
parser.add_argument("-dir", help="nginx conf dir", type=str, required=False)


if __name__ == "__main__":
    args = parser.parse_args()
    if args.action is None:
        sys.exit(1)
    if args.action == "http_server":
        http_server.app.run("0.0.0.0", port=12345)
    elif args.action == "tool":
        if args.dir is None:
            raise Exception("no dir")
        conf_dir = args.dir
        parser = parse.NGINXDirParse(conf_dir)
        ret = parser.parse()
        print(ret)
    else:
        raise Exception("action not support")
