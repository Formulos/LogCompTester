import os
import subprocess
import re

def auto_issue(person,text):
    subprocess.run(["ghi", "open","-m","autoIssue 2.4\n"+text],cwd="src/{!s}".format(person))


if __name__ == '__main__':
    DIR = "reports/"
    file_list = ([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    for f in file_list:
        name = f[:-4] #tira o .txt

        with open("reports/{!s}".format(f), 'r') as file:
            data = file.read()

        auto_issue(name,data)