import os
import sys
import subprocess
import re
import json

#Constantes
accepted_languages = ["python3","rust","C++","C#"]
compile_languages = ["C++","C#"]
maxtime=30.0 #Timeout para cada teste, em segundos
direct_input = True # passa o conteudo do arquivo como argumento (testes das versões baixas)
assembly = False
assembly_test = 1
extension = ".txt"

def test_main(DIR,student):
    language = student["language"]
    person = student["student_username"]
    repo = student["repository_name"]
        
    args = student["run_args"]
    args = args.split()
    
    if (language not in accepted_languages):
        raise Exception("language {!s} is not a accepted language!".format(language))
    
    #diz a quantidade de testes, simplesmente pega a quantidade de arquivos na pasta e divide por dois
    size_test = (len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]))//2

    src_file = "src/{!s}".format(person)

    report = '{}/{}\n'.format(person,repo)

    failed_test = False

    args.append("")


    if language in compile_languages :
        compile_args = student["compile_args"]
        compile_args = compile_args.split()
        compile_err_output = compile(src_file,compile_args)

        if compile_err_output: #strings vazias são falsas
            report += "Error: teste automatico não conseguiu compilar arquivo!\n"
            report += "parametros de compilação: {!s}\n".format(" ".join(compile_args))
            report += "erro de compilação:{!s}".format(compile_err_output)
            report_writer(report,person)
            return True

    #caso seja a versão 3.0
    if assembly:
        test_file = os.path.abspath(DIR +"/teste{!s}".format(assembly_test) + extension)
        #stdin_file = os.path.abspath(DIR +"/inputs/input{!s}.txt".format(i))
        #sol_file = DIR +"/sol{!s}.txt".format(i)
        args[-1] = test_file
        try:
            output,output_error = get_program_output(src_file,language,args)
            if output_error:
                print(output_error)
                return True
            return False
        except subprocess.TimeoutExpired:
            print("Assemble timeout")
            return True
    
    for i in range(1,size_test + 1):
        test_file = os.path.abspath(DIR +"/teste{!s}".format(i) + extension)
        stdin_file = os.path.abspath(DIR +"/inputs/input{!s}.txt".format(i))
        sol_file = DIR +"/sol{!s}".format(i) + extension


        if direct_input:
            test_file = os.path.abspath(DIR +"/teste{!s}.txt".format(i))
            args[-1] = get_text(test_file).encode()
        else:
            args[-1] = test_file

        input_test = get_text(test_file)


        #data_encoded = str.encode(data)

        
        test_stdin = None
        #caso um input exista
        if (os.path.exists(stdin_file)):
            test_stdin = get_text(stdin_file)
            test_stdin = test_stdin.encode()

        try:
            output,output_error = get_program_output(src_file,language,args,test_stdin)
        except subprocess.TimeoutExpired:
            report += "teste{!s}: falha\n".format(str(i))
            report = write_input_stdin(report,input_test,test_stdin)
            report += "Timeout, teste demorou mais de {} segundo para rodar, assumo que entrou em um loop infinito\n\n".format(str(maxtime))
            failed_test = True
            continue
            

        if ((not output) and (not output_error)):
            report += "teste{!s}: falha\n".format(str(i))
            report = write_input_stdin(report,input_test,test_stdin)
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
                report = write_input_stdin(report,input_test,test_stdin)
                report += "output esperado: \n{!s}\n\noutput recebido: \n\n{!s}\n\n".format(str(sol),str(output))
                failed_test = True
                if (output_error):
                    report += "Mas algo saiu no stderror(que não deveria): \n{!s}\n\n".format(str(output_error))
                else:
                    report += "\n"    

        #cuida dos testes de erro
        else: #ou seja sol==Error
            if (not output_error): # lembrando que strings vazias são falsas
                report += "teste{!s}: falha, não deu erro mais deveria (algo deveria ter saido no stderr)\n".format(str(i))
                report = write_input_stdin(report,input_test,test_stdin)
                failed_test = True
            
    if failed_test:
        report_writer(report,person)

    return failed_test

def assertEquals(var1, var2):
    return var1 == var2

def get_text(read_file):
    with open(read_file, 'r') as file:
        data = file.read()
    return data

def write_input_stdin(report,input_test,test_stdin):
    
    report +="input do teste: \n```\n\n{!s}\n```\n\n".format(str(input_test))
    if test_stdin:
        test_stdin = test_stdin.decode()
        report +="stdin do teste: \n{!s}\n".format(str(test_stdin))
    return report

def get_program_output(src_file,language,args,test_stdin=None):
    
    output = subprocess.run(args,cwd=src_file,input=test_stdin,stderr=subprocess.PIPE,stdout=subprocess.PIPE,timeout=maxtime)

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
    text2 = ""
    for i in text.splitlines():
        text2 += i.strip()+"\n"
    text2=text2[:-1]

    return text2

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
