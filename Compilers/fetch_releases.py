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

CODE_VERSION = sys.argv[2]
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

def update_repos(students, code_version): 
    for student in students:
        student_name = student["student_username"]
        student_repo = student["repository_name"]
        clone_path = f"{CLONE_BASE_PATH}/{student_name}"
        git_path = f"{GIT_BASE_URL}{student_name}/{student_repo}.git"

        if (not os.path.isdir(f"{clone_path}/.git")):
            clone_repo(student_name, clone_path, git_path, code_version)
        
        else:
            print(clone_path)
            cur_repo = Repo(clone_path)
            cur_repo.git.reset('--hard')
            cur_repo.remotes.origin.pull("master")
        

        checkout_version(clone_path, student_name, code_version)

def checkout_version(clone_path, student_name, code_version):
    cur_repo = Repo(clone_path)
    
    try:
        latest_version = get_latest_minor_release(cur_repo, code_version)
    except:
        print("Could not get the latest version, does this student have any releases available?")
        report_writer("Aluno: {!s}\nRelease {!s}.* não encontrada!\nVoce fez alguma Release?".format(student_name,code_version),student_name)
        return

    print(f"checking out version {latest_version} from {student_name}")
    if latest_version != '0':
        Git(clone_path).checkout(latest_version)
    else:
        print(f"student {student_name} does not have this version available!")
        report_writer("Aluno: {!s}\nRelease {!s}.* não encontrada!".format(student_name,code_version),student_name)

def get_latest_minor_release(cur_repo, code_version):
    f_code_ver = re.sub("[a-zA-Z]+", "", code_version)
    return sorted([v.name if (f_code_ver.split('.')[0] is re.sub("[a-zA-Z]+", "", v.name).split('.')[0] and \
        f_code_ver.split('.')[1] is re.sub("[a-zA-Z]+", "", v.name).split('.')[1]) 
        else str(0) \
        for v in cur_repo.tags])[-1]

def clone_repo(student_name, clone_path, git_path, code_version):
        print(f"cloning from {student_name}")
        print(clone_path)
        Repo.clone_from(git_path, clone_path)

def delete_old_reports():
    filelist = [ f for f in os.listdir("reports/") if f.endswith(".txt") ]
    for f in filelist:
        os.remove(os.path.join("reports/", f))

def delete_old_src():
    filelist = [ f for f in os.listdir("src/")]
    for f in filelist:
        shutil.rmtree(os.path.join("src/", f))

def report_writer(report,person):
    person_file = "reports/{!s}.txt".format(person)
    with open(person_file, 'w') as file:
        file.write(report)

if __name__ == "__main__":
    delete_old_reports()
    delete_old_src()
    update_repos(read_git_url_json(), CODE_VERSION)