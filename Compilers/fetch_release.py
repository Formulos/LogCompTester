from git import Repo, Git
import sys
import os
import shutil
import re
import json

"""
important:
esse codigo deleta tudo que esta dentro das pastas src e reports
"""

GIT_BASE_URL = "git@github.com:"
CLONE_BASE_PATH = f"src/"

# get ssh key
git_ssh_identity_file = os.path.expanduser('~/.ssh/id_rsa')
git_ssh_cmd = 'ssh -i %s' % git_ssh_identity_file
old_env = Git().custom_environment(GIT_SSH_COMMAND=git_ssh_cmd) #make git use said ssh key
# old_env = environment before the use of ssh key

def read_git_url_json():
    with open(sys.argv[1]) as git_urls:
        return json.load(git_urls)

def update_repos(git_username, repository, release): 
    clone_path = f"{CLONE_BASE_PATH}/{git_username}/{repository}"
    git_path = f"{GIT_BASE_URL}{git_username}/{repository}.git"

    if (not os.path.isdir(f"{clone_path}/.git")):
        clone_repo(git_username, clone_path, git_path)
    
    else:
        print(clone_path)
        cur_repo = Repo(clone_path)
        cur_repo.git.reset('--hard')
        cur_repo.remotes.origin.pull("master")
    
    Git(clone_path).checkout(release)

def clone_repo(git_username, clone_path, git_path):
        print(f"cloning from {git_username}")
        print(clone_path)
        Repo.clone_from(git_path, clone_path)

def check_dir():
    if (os.getcwd()[-9:] != 'Compilers'):
        print(
            """----Cuidado----
        esse codigo foi escrito para funcionar dentro da pasta Compiler,
        varios caminhos estão relativos, portanto a chance de dar erro é alta.
        pasta atual: {}
        --------""".format(os.getcwd()))

def create_src(git_username):
    if not (os.path.isdir('./src')):
        os.mkdir("./src")
    user_path = os.path.join('./src', git_username)
    if not (os.path.isdir(user_path)):
        os.mkdir(user_path)

def delete_old_src(git_username, repository):
    rep = os.path.join("src/", git_username, repository)
    if os.path.isdir(rep):
        shutil.rmtree(rep)

def report_writer(report,person):
    person_file = "reports/{!s}.txt".format(person)
    with open(person_file, 'w') as file:
        file.write(report)

if __name__ == "__main__":

    if len(sys.argv) < 4:
        raise ValueError('USAGE: python3 fetch_release.py GIT_USER REPOSITORY RELEASE')

    git_username = sys.argv[1]
    repository = sys.argv[2]
    release = sys.argv[3]

    check_dir()
    create_src(git_username)
    delete_old_src(git_username, repository)
    update_repos(git_username, repository, release)
