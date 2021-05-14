import sqlite3

DB_FILE = 'db/compilers.db'

def getConnection(db_file = None):
    if db_file is None:
        db_file = DB_FILE
    conn = sqlite3.connect(db_file)

    conn.execute("PRAGMA foreign_keys = 1")

    return conn

def getResults(sql):
    conn = getConnection()
    
    cursor = conn.cursor()
    cursor.execute(sql)
    regs = cursor.fetchall()
    
    conn.close()

    return(regs)

def executeCommitQuery(sql):
    conn = getConnection()
    
    cursor = conn.cursor()
    cursor.execute(sql)
    
    conn.commit()
    conn.close()


def get_repo_release_status(git_username, repository):
    sql = 'SELECT * ' + \
            'FROM release_status rs ' + \
           'WHERE rs.git_username = "{}" '.format(git_username) + \
             'AND rs.repository_name = "{}" '.format(repository)  + \
           'ORDER BY rs.version_name ASC'

    res = getResults(sql)
    return res


def record_test_result(version_name, release_name, git_username, repository_name, test_status, issue_text):

    sql =  'INSERT INTO test_result (version_name, release_name, git_username, repository_name, date_run, test_status, issue_text) ' + \
        'VALUES("{}", "{}", "{}", "{}", date("now"), "{}", "{}");'.format(version_name, release_name, git_username, repository_name, test_status, issue_text)

    executeCommitQuery(sql)


def get_compile_args(git_username, repository):
    return ''

def get_run_args(git_username, repository):
    sql = 'SELECT program_call ' + \
            'FROM repository rep ' + \
           'WHERE rep.git_username = "{}" '.format(git_username) + \
             'AND rep.repository_name = "{}" '.format(repository)

    res = getResults(sql)
    return res[0][0]

def get_language(git_username, repository):
    sql = 'SELECT language ' + \
            'FROM repository rep ' + \
           'WHERE rep.git_username = "{}" '.format(git_username) + \
             'AND rep.repository_name = "{}" '.format(repository)

    res = getResults(sql)
    return res[0][0]

def get_direct_input(version_name):
    sql = 'SELECT direct_input ' + \
            'FROM version ver ' + \
           'WHERE ver.version_name = "{}" '.format(version_name)

    res = getResults(sql)
    return res[0][0]

def get_extension(version_name):
    sql = 'SELECT extension ' + \
            'FROM version ver ' + \
           'WHERE ver.version_name = "{}" '.format(version_name)

    res = getResults(sql)
    return res[0][0]
    