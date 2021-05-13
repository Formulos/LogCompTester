import os
import sys
import subprocess
import re
import json
import db.db_conn as db
import issuer_pusher as ip

#Constantes
accepted_languages = ["python","rust_cargo","C++","C#"]
compile_languages = ["C++","C#"]
maxtime = 30.0 #Timeout para cada teste, em segundos
assembly = False
assembly_test = 1
#extension = '.txt'

def test_main(DIR, git_username, repository, release, version):    
    args = db.get_run_args(git_username, repository)
    args = args.split()

    language = db.get_language(git_username, repository)
    direct_input = db.get_direct_input(version)
    extension = db.get_extension(version)
    
    if (language not in accepted_languages):
        raise Exception("language {!s} is not a accepted language!".format(language))
    
    #diz a quantidade de testes, simplesmente pega a quantidade de arquivos na pasta e divide por dois
    size_test = (len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]))//2

    src_file = "src/{!s}/{!s}".format(git_username, repository)

    report = '{}/{}\n'.format(git_username,repository)

    failed_test = False

    args.append("")


    if language in compile_languages :
        compile_args = db.get_compile_args(git_username, repository)
        compile_args = compile_args.split()
        compile_err_output = compile(src_file,compile_args)

        if compile_err_output: #strings vazias são falsas
            report += "Error: teste automatico não conseguiu compilar arquivo!\n"
            report += "parametros de compilação: {!s}\n".format(" ".join(compile_args))
            report += "erro de compilação:{!s}".format(compile_err_output)
            
            db.record_test_result(version_name = version, release_name = release, git_username = git_username, repository_name = repository, test_status = 'ERROR', issue_text = report)
            ip.push_issue(git_username, repository, release, text = report)
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
        report = report.replace('"', '\'')
        db.record_test_result(version_name = version, release_name = release, git_username = git_username, repository_name = repository, test_status = 'FAILED', issue_text = report)
        ip.push_issue(git_username, repository, release, text = report)
    else:
        db.record_test_result(version_name = version, release_name = release, git_username = git_username, repository_name = repository, test_status = 'PASS', issue_text = '')

    return failed_test

def assertEquals(var1, var2):
    return var1 == var2

def get_text(read_file):
    with open(read_file, 'r', encoding='utf8') as file:
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

if __name__ == '__main__':

    if len(sys.argv) < 4:
        raise ValueError('USAGE: python3 auto_test.py GIT_USER REPOSITORY RELEASE')
    
    git_username = sys.argv[1]
    repository = sys.argv[2]
    release = sys.argv[3]
    version = release[0:4]

    test_folder = release[1:4]

    direct_input = db.get_direct_input(version)
    if not direct_input:
        test_folder = 'C/{}'.format(release[1:4])

    test_dir = "tests/{!s}_tests".format(test_folder)
    
    print(git_username)
    error = test_main(test_dir,git_username,repository,release,version)
    print("algum erro?: ",error)
    print("\n")
