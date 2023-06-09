import sys
import os
file_path = os.path.dirname(os.path.abspath(__file__))
print(__file__, file_path)
lib_path = os.path.join(os.path.dirname(file_path), "src")
print(lib_path)
sys.path.insert(0, lib_path)
import pytest

from conf_parse import parse
import json


def test_case1():
    parser = parse.NGINXDirParse("./test_cases/t1")
    ret = parser.parse()
    print(json.dumps(ret))

if __name__ == "__main__":
    #parser = parse.NGINXFileParser("/Users/11133435/PycharmProjects/NGINXConfToA6/test/test_cases/t1/conf.d/server1.conf")
    parser = parse.NGINXDirParse("./test_cases/t1")
    ret = parser.parse()
    print(json.dumps(ret))