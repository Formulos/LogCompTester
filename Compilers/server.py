from flask import Flask, request, abort, json, Response
from git import Repo, Git
from github import Github
from flask import send_file
import json
import os
import sys
import shutil
import re
import subprocess
import svg_report as sr
import time
import hashlib

app = Flask(__name__)


BASE_DIR = '/home/ubuntu/LogCompTester/Compilers'

os.chdir(BASE_DIR)

@app.route('/webhook', methods=['POST'])
def api_webhook():
    os.chdir(BASE_DIR)
    if request.method == 'POST':
        if request.content_type == 'application/json':
            with open('payload.json', 'w') as output:
                json.dump(request.json, output)
            if "release" in request.json:
                if request.json["action"] == "created":
                    git_username = request.json["release"]["author"]["login"]
                    repository_name = request.json["repository"]["name"]
                    version = request.json["release"]["tag_name"]
                    print(f'git_username: {git_username}, repository_name: {repository_name}, version: {version}')
                    os.system(f'python3 full_proc.py {git_username} {repository_name} {version} &')
            else:
                git_username = request.json["repository"]["owner"]["login"]
                repository_name = request.json["repository"]["name"]
                version = request.json["ref"]
                print(f'git_username: {git_username}, repository_name: {repository_name}, version: {version}')
                os.system(f'python3 full_proc.py {git_username} {repository_name} {version} &')
        return 'success', 200
    else:
        abort(400)

@app.route('/')
def test():
    return 'Hello World'

@app.route('/svg/<user>/<repo>/', methods=['GET'])
def svg(user, repo):
    report = sr.RepoReport(git_username = user, repository_name = repo)
    svg = report.compile()
    resp = Response(response=svg, status=200, mimetype="image/svg+xml")
    resp.headers['Cache-Control'] = 'no-cache'
    resp.headers['Pragma'] = 'no-cache'

    now = time.strftime("%Y %m %d %H %M")
    txt = '{} {} {}'.format(user, repo, now).encode('utf-8')
    etag = hashlib.sha1(txt).hexdigest()
    resp.headers['ETag'] = etag
    
    return resp
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True)
