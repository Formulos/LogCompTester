import os
import sys
from github import Github

def push_issue(git_username, repository, release, text):
    token = os.getenv('GITHUB_TOKEN', '...')
    g = Github(token)
    repo = g.get_repo('{}/{}'.format(git_username, repository))
    i = repo.create_issue(title="Problemas na {}".format(release),
                            body=text,
                            assignee=git_username)