import db_conn as db

conn = db.getConnection('compilers.db')

cursor = conn.cursor()

#############################################
#  GIT USERS
#############################################
cursor.execute("PRAGMA foreign_keys = 0")

cursor.execute("""DROP TABLE IF EXISTS test_result;""")
cursor.execute("""DROP TABLE IF EXISTS users;""")
cursor.execute("""DROP TABLE IF EXISTS repository;""")
cursor.execute("""DROP TABLE IF EXISTS version;""")

cursor.execute("""DROP VIEW IF EXISTS release_status;""")
cursor.execute("""DROP VIEW IF EXISTS test_result_status;""")

cursor.execute("PRAGMA foreign_keys = 1")

cursor.execute("""
CREATE TABLE users (
    git_username TEXT PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    surname TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE repository (
    git_username TEXT NOT NULL,
    repository_name TEXT NOT NULL,
    language TEXT NOT NULL,
    compiled INTEGER check(compiled = 0 or compiled = 1),
    program_call TEXT NOT NULL,
    PRIMARY KEY(git_username, repository_name),
    FOREIGN KEY(git_username) REFERENCES users(git_username)
);
""")

cursor.execute("""
CREATE TABLE version (
    version_name TEXT PRIMARY KEY NOT NULL,
    direct_input INTEGER NOT NULL,
    extension TEXT NOT NULL,
    date_from DATETIME NOT NULL,
    date_to   DATETIME NOT NULL
);
""")

cursor.execute("""
CREATE TABLE test_result (
    version_name TEXT NOT NULL,
    release_name TEXT NOT NULL,
    git_username TEXT NOT NULL,
    repository_name TEXT NOT NULL,
    date_run DATETIME NOT NULL,
    test_status TEXT check(test_status = 'PASS' or test_status = 'ERROR' or test_status = 'FAILED'),
    issue_text TEXT,
    PRIMARY KEY(version_name, release_name, git_username, repository_name),
    FOREIGN KEY(version_name) REFERENCES version(version_name),
    FOREIGN KEY(repository_name, git_username) REFERENCES repository(repository_name, git_username)   
);
""")

conn.commit()

#############################################
#  VIEW RELEASE STATUS
#############################################
cursor.execute("""
CREATE VIEW test_result_status AS
    SELECT tes.git_username,
            tes.repository_name,
            tes.version_name,
            max(tes.test_status) AS test_status
       FROM test_result tes
  LEFT JOIN version as ver ON ver.version_name = tes.version_name
   GROUP BY tes.git_username, tes.repository_name, tes.version_name
   ORDER BY tes.git_username, tes.repository_name
""")

# view with current status of each avaiable version (date_from < today), for each student
cursor.execute("""
CREATE VIEW release_status AS
       SELECT rep.git_username,
              ver.version_name,
              rep.repository_name,
              CASE trs.test_status is null
                  WHEN 1
                     THEN 'NOT_FOUND'
                  ELSE trs.test_status
              END test_status,
              CASE trs.test_status is null OR trs.test_status = 'ERROR'
                  WHEN 1
                     THEN CASE date('now') > ver.date_to
                             WHEN 1
                                THEN 'DELAYED'
                             ELSE 'ON_TIME'
                          END
                  ELSE (SELECT CASE min(date_run) > ver.date_to
                                     WHEN 1
                                        THEN 'DELAYED'
                                     ELSE 'ON_TIME'
                                END
                          FROM test_result tes
                         WHERE tes.repository_name = rep.repository_name
                           AND tes.version_name = ver.version_name
                           AND tes.git_username = rep.git_username
                           AND tes.test_status = 'PASS')
              END delivery_status
         FROM repository AS rep,
              version AS ver
    LEFT JOIN test_result_status AS trs ON trs.version_name = ver.version_name
                                       AND trs.git_username = rep.git_username
                                       AND trs.repository_name = rep.repository_name
        WHERE ver.date_from < date('now')
     ORDER BY rep.git_username, trs.repository_name
""")

conn.commit()

conn.close()