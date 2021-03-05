import os
import sys
from github import Github

token = os.getenv('GITHUB_TOKEN', '...')

g = Github(token)

if __name__ == '__main__':
    DIR = "reports/"
    file_list = ([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    
    if len(sys.argv) < 2:
    	print(len(sys.argv))
    	print(sys.argv)
    	raise IndexError('O parâmetro de versão não foi informado.')
    else:
    	version = sys.argv[1]
    
    for f in file_list:
        name = f[:-4] #tira o .txt

        with open("reports/{!s}".format(f), 'r') as file:
            repo = file.readline().strip()
            text = file.read()

        repo = g.get_repo(repo)
        i = repo.create_issue(title="Problemas na {}".format(version),
                              body=text,
                              assignee=name)
