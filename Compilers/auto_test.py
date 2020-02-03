import os
import subprocess
import re
import json
#from subprocess import PIPE



def test_main(person,DIR):
    
    size_test = (len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])) //2
    src_file = "src/{!s}/main.py".format(person)

    report = "Aluno: {!s}\n \n".format(person)

    failed_test = False

    for i in range(1,size_test + 1):
        test_file = DIR +"/teste{!s}.txt".format(i)
        sol_file = DIR +"/sol{!s}.txt".format(i)

        data = get_text(test_file)
        data_encoded = str.encode(data)

        output = get_program_output(data_encoded,src_file)

        sol = get_text(sol_file)
        sol = os.linesep.join([s for s in sol.splitlines() if s])

        first_digit = re.search(r"\d", output)
        first_digit = first_digit.start()
        output = output[first_digit:]

        result = assertEquals(int(sol), int(output))
        if result:
            report += "teste{!s}: ok\n \n".format(str(i))
        else:
            report += "teste{!s}: falha\n".format(str(i))
            report += "input do teste: {!s}".format(str(data))
            report += "output esperado: {!s} | output recebido:{!s}\n \n".format(str(sol),str(output))
            failed_test = True

    if failed_test:
        report_writer(report,person)


def assertEquals(var1, var2):
    return var1 == var2

def get_text(test_file):
    with open(test_file, 'r') as file:
        data = file.read()
    return data

def get_program_output(data,src_file):
    output = subprocess.run(["python3",src_file],input = data,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
    text = output.stdout.decode("utf-8")
    text = os.linesep.join([s for s in text.splitlines() if s])
    text.strip()

    return text

def delete_old_reports():
    filelist = [ f for f in os.listdir("reports/") if f.endswith(".txt") ]
    for f in filelist:
        os.remove(os.path.join("reports/", f))

def report_writer(report,person):
    person_file = "reports/relatorio_{!s}.txt".format(person)
    with open(person_file, 'w') as file:
        file.write(report)

def read_git_url_json():
    with open("git_paths.json") as git_urls:
        return json.load(git_urls)


if __name__ == '__main__':
    test_dir = "tests/1.0_tests"
    delete_old_reports()

    json_file = read_git_url_json()


    for student in json_file:
        p = student["student_username"]
        #language = student["language"]

        print(p)
        test_main(p,test_dir)