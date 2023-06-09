import sys
import os
import json
import uuid

from flask import Flask
from flask import render_template
from flask import request


from conf_parse import parse


UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/index.html", methods=["GET", "POST"])
def index():
    method = request.method
    if method == "GET":
        return render_template("index.html")
    elif method == "POST":
        # print(request.data)
        if 'file' not in request.files:
            return "no file"
        file = request.files['file']
        if file:
            tmp_dir = str(uuid.uuid1())
            dir_path = os.path.join(app.config['UPLOAD_FOLDER'], tmp_dir)
            if not os.path.exists(dir_path):
                os.mkdir(dir_path, 0o755)
            file_path = os.path.join(dir_path, "nginx.conf")
            file.save(file_path)
            parser = parse.NGINXFileParser(file_path)
            parser.convert()
            ret = parser.output()
            print(json.dumps(ret))
            html_data = []
            with open(file_path, encoding="utf-8") as f:
                for cnt, line in enumerate(f.readlines()):
                    tmp_dict = {
                        'content': line,
                        'color': cnt % 2,
                        'line_num': cnt + 1
                    }
                    html_data.append(tmp_dict)
            # print(read_data)
            return render_template("nginx_file.html", data=html_data)


@app.route("/test11")
def parse_file_test():
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test/test_cases/t1/nginx.conf")
    parser = parse.NGINXFileParser(None, file_path)
    parser.convert()
    ret = parser.output()
    print(json.dumps(ret))
    html_data = []
    with open(file_path, encoding="utf-8") as f:
        for cnt, line in enumerate(f.readlines()):
            tmp_dict = {
                'content': line,
                'color': cnt%2,
                'line_num': cnt + 1
            }
            html_data.append(tmp_dict)
    #print(read_data)
    return render_template("nginx_file.html", data=html_data)
