from flask import Flask, request, abort, json
from git import Repo, Git
from github import Github
import json
import os
import sys
import shutil
import re
import subprocess

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def api_webhook():
    if request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            with open('payload.json', 'w') as output:
                json.dump(request.json, output)
            if "release" in request.json:
                if request.json["action"] == "created":
                    git_username = request.json["release"]["author"]["login"]
                    repository_name = request.json["repository"]["name"]
                    version = request.json["release"]["tag_name"]
            else:
                git_username = request.json["repository"]["owner"]["login"]
                repository_name = request.json["repository"]["name"]
                version = request.json["ref"]
            print(f'git_username: {git_username}, repository_name: {repository_name}, version: {version}')
            os.system(f'python3 full_proc.py {git_username} {repository_name} {version} &')
        return 'success', 200
    else:
        abort(400)
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)