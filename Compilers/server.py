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

app = Flask(__name__)

os.chdir('/home/ubuntu/LogCompTester/Compilers')

@app.route('/webhook', methods=['POST'])
def api_webhook():
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
                    os.system(f'cd ~/LogCompTester/Compilers;python3 full_proc.py {git_username} {repository_name} {version} &')
            else:
                git_username = request.json["repository"]["owner"]["login"]
                repository_name = request.json["repository"]["name"]
                version = request.json["ref"]
                print(f'git_username: {git_username}, repository_name: {repository_name}, version: {version}')
                os.system(f'cd ~/LogCompTester/Compilers;python3 full_proc.py {git_username} {repository_name} {version} &')
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
    return Response(response=svg, status=200, mimetype="image/svg+xml")
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True)
