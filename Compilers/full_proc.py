import os
import sys
import random


if __name__ == "__main__":
    git_username = sys.argv[1]
    repository = sys.argv[2]
    release = sys.argv[3]

    #sec = random.randrange(1, 10)
    #os.system('sleep {}'.format(sec))

    fetch_command = 'python3 fetch_release.py {} {} {}'.format(git_username, repository, release)
    res = os.system(fetch_command)

    if res == 0:
        fetch_command = 'python3 auto_test.py {} {} {}'.format(git_username, repository, release)
        os.system(fetch_command)
