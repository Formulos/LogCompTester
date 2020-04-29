import os
import sys
import subprocess
import re
import json
#from subprocess import PIPE

acepeted_languages = ["python3","C++","C#"] # C# so funciona se um executavel ja existir
compile_languages = ["C++"] # C# so funciona com dotnet run


def test_main(DIR,student):
    language = student["language"]
    person = student["student_username"]
    args = student["run_args"]
    args = args.split()
    
    if (language not in acepeted_languages):
        raise Exception("language {!s} is not a acepeted language!".format(language))
    
    size_test = (len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])) //2
    src_file = "src/{!s}".format(person)

    report = "Aluno: {!s}\n \n".format(person)

    failed_test = False

    args.append("")

    if language in compile_languages :
        compile_args = student["compile_args"]
        compile_args = compile_args.split()
        #compile_args.append("-w") #supress C++ warnings
        compile_err_output = compile(src_file,compile_args)

        if compile_err_output: #strings vazias são falsas
            report += "Error: teste automatico não conseguio compilar arquivo!\n"
            report += "parametros de compilação: {!s}\n".format(" ".join(compile_args))
            report += "erro de compilação:{!s}".format(compile_err_output)
            report_writer(report,person)
            return True

    for i in range(1,size_test + 1):
        test_file = os.path.abspath(DIR +"/teste{!s}.php".format(i))
        sol_file = DIR +"/sol{!s}.php".format(i)

        input_test = get_text(test_file)
        #args[-1] = data
        args[-1] = data = test_file
        #data_encoded = str.encode(data)

        try:
            output,output_error = get_program_output(src_file,language,args)
        except subprocess.TimeoutExpired:
            report += "teste{!s}: falha\n".format(str(i))
            report += "input do teste: \n \n{!s}\n \n ".format(str(input_test))
            report += "Timeout, teste demorou mais de 3 segundo para rodar, assumo que entrou em um loop infinito\n\n"
            failed_test = True
            continue
            

        if (output == "") and (output_error == ""):
            report += "teste{!s}: falha\n".format(str(i))
            report += "input do teste: \n \n{!s}\n \n ".format(str(input_test))
            report += "não recebi nada de output!(stderr e stdout estão vazios e não deveriam)\n\n"
            failed_test = True
            #print(output)
            continue

        sol = get_text(sol_file)
        sol = text_processor(sol)

        output = text_processor(output)
        output_error = text_processor(output_error)

        if sol != "Error": #cuida dos testes "normais" (os que não são de erro)

            result = assertEquals(sol, output)
            if not result:
                report += "teste{!s}: falha\n".format(str(i))
                report += "input do teste: \n \n{!s}\n \n \n".format(str(input_test))
                report += "output esperado: \n \n{!s}\n \noutput recebido: \n \n{!s}\n \n\n".format(str(sol),str(output))
                failed_test = True
                if (output_error):
                    report += "Mas algo saiu no stderror(que não deveria): \n \n{!s}\n \n\n".format(str(output_error))
                else:
                    report += "\n"    

        #cuida dos testes de erro
        else: #aka if sol=Error
            if (not output_error): # lembrando que strings vazias são falsas
                # o codigo não gerou um erro quando deveria
                report += "teste{!s}: falha, não deu erro mais deveria (algo deveria ter saido no stderr)\n".format(str(i))
                report += "input do teste: \n \n{!s}\n \n ele deveria dar erro!\n\n".format(str(input_test))
                failed_test = True
            

    if failed_test:
        report_writer(report,person)

    return failed_test

def assertEquals(var1, var2):
    return var1 == var2

def get_text(test_file):
    with open(test_file, 'r') as file:
        data = file.read()
    return data

def get_program_output(src_file,language,args,maxtime=3.0):
    #if language =="python3":
    #    args = ["python3",src_file,data]

    output = subprocess.run(args,cwd=src_file,stderr=subprocess.PIPE,stdout=subprocess.PIPE,timeout=maxtime)

    text = output.stdout.decode("utf-8")
    text_error = output.stderr.decode("utf-8")
    text = text_processor(text)

    return text,text_error

def compile(src_file,compile_args):
    output = subprocess.run(compile_args,cwd=src_file,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
    text = output.stderr.decode("utf-8")

    return text

def text_processor(text):
    text = os.linesep.join([s for s in text.splitlines() if s]) #tira espaços seguidos (\n\n)
    text.strip()

    return text

def report_writer(report,person):
    person_file = "reports/{!s}.txt".format(person)
    with open(person_file, 'w') as file:
        file.write(report)


def read_git_url_json():
    with open("git_paths.json") as git_urls:
        return json.load(git_urls)


if __name__ == '__main__':
    test_dir = "tests/{!s}_tests".format(sys.argv[1])
    

    json_file = read_git_url_json()


    for student in json_file:
        person = student["student_username"]
        
        
        if (not os.path.exists("reports/{!s}.txt".format(person))):
            print(person)
            error = test_main(test_dir,student)
            print("algum erro?: ",error)
            print("\n")