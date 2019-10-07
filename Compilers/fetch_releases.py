from git import Repo, Git
import sys
import os
import re
import json

CODE_VERSION = sys.argv[2]
GIT_BASE_URL = "git://github.com/"
CLONE_BASE_PATH = f"src/{CODE_VERSION}"

def read_git_url_json():
    with open(sys.argv[1]) as git_urls:
        return json.load(git_urls)

def update_repos(students, code_version):
    for student in students:
        student_name = student["student_username"]
        student_repo = student["repository_name"]
        clone_path = f"{CLONE_BASE_PATH}/{student_name}"
        git_path = f"{GIT_BASE_URL}{student_name}/{student_repo}.git"

        if (os.path.isdir(f"{clone_path}/.git")):
            checkout_version(clone_path, student_name, code_version)
        else:
            clone_repo(student_name, clone_path, git_path, code_version)

def checkout_version(clone_path, student_name, code_version):
    cur_repo = Repo(clone_path)
    latest_version = get_latest_minor_release(cur_repo, code_version)
    print(f"checking out version {latest_version} from {student_name}")
    
    if latest_version != '0':
        Git(clone_path).checkout(latest_version)
    else:
        print("student {student_name} does not have this version available!")

def get_latest_minor_release(cur_repo, code_version):
    f_code_ver = re.sub("[a-zA-Z]+", "", code_version)
    return sorted([v.name if (f_code_ver.split('.')[0] is re.sub("[a-zA-Z]+", "", v.name).split('.')[0] and \
        f_code_ver.split('.')[1] is re.sub("[a-zA-Z]+", "", v.name).split('.')[1]) 
        else str(0) \
        for v in cur_repo.tags])[-1]

def clone_repo(student_name, clone_path, git_path, code_version):
        print(f"cloning from {student_name}")
        Repo.clone_from(git_path, clone_path)

if __name__ == "__main__":
    update_repos(read_git_url_json(), CODE_VERSION)