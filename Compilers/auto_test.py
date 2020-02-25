import os
import sys
import subprocess
import re
import json
#from subprocess import PIPE



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

    if language == "C++": #refatorar esse codigo, varias linguas
        compile_args = student["compile_args"]
        compile_args = compile_args.split()
        compile_args.append("-w") #supress warnings
        output = compile(src_file,compile_args)

        if output: #strings vazias são falsas
            report += "Error: teste automatico não conseguio compilar arquivo!\n"
            report += "parametros de compilação: {!s}\n".format(" ".join(compile_args))
            report += "erro de compilação:{!s}".format(output)
            report_writer(report,person)
            return True

    for i in range(1,size_test + 1):
        test_file = DIR +"/teste{!s}.txt".format(i)
        sol_file = DIR +"/sol{!s}.txt".format(i)

        data = get_text(test_file)
        args[-1] = data
        #data_encoded = str.encode(data)

        try:
            output,output_error = get_program_output(src_file,language,args)
        except subprocess.TimeoutExpired:
            report += "teste{!s}: falha\n".format(str(i))
            report += "input do teste: {!s} ".format(str(data))
            report += "Timeout, teste demorou mais de 3 segundo para rodar, assumo que entrou em um loop infinito\n\n"
            
            

        if (output == "") and (output_error == ""):
            report += "teste{!s}: falha\n".format(str(i))
            report += "input do teste: {!s} ".format(str(data))
            report += "não recebi nada de output!(stderr e stdout estão vazios e não deveriam)\n"
            failed_test = True
            #print(output)
            continue

        sol = get_text(sol_file)
        sol = text_processor(sol)

        if sol != "Error": #cuida dos testes "normais" (os que não dão erro)
            try: #esse bloco tenta limpar o output
                first_digit = re.search(r"\d", output) #lida com texto aleatorio das versão 1.0
                first_digit = first_digit.start() 
            except: #tratar o erro do mesmo jeito que o outro
                report += "teste{!s}: falha\n".format(str(i))
                report += "O stdout saiu vazio quando não deveria \n"
                report += "input do teste: {!s} \n".format(str(data))
                report += "output esperado: {!s} | output recebido:{!s}\n".format(str(sol),str(output))
                if (output_error):
                    report += "Mas algo saiu no stderror(que não deveria): \"{!s}\" \n \n".format(str(output_error))
                else:
                    report += "\n"
                failed_test = True
                continue

            if output[first_digit-1] == "-": # não sei se tem jeito melhor que esse
                first_digit -= 1 # feito para não ignorar numeros negativos

            output = output[first_digit:]
            output = text_processor(output)

            result = assertEquals(sol, output)
            if not result:
                report += "teste{!s}: falha\n".format(str(i))
                report += "input do teste: {!s} \n".format(str(data))
                report += "output esperado: {!s} | output recebido:{!s}\n \n".format(str(sol),str(output))
                failed_test = True
            if (output_error):
                report += "teste{!s}: recebeu um erro inesperado (algo saio no stderr quando não deveria)\n".format(str(i))
                report += "saida do stderr: {!s} \n \n".format(str(output_error))
                failed_test = True

        #cuida dos testes de erro
        else: #aka if sol=Error
            if (not output_error): # lembrando que strings vazias são falsas
                # o codigo não gerou um erro quando deveria
                report += "teste{!s}: falha, não deu erro mais deveria (algo deveria ter saido no stderr)\n".format(str(i))
                report += "input do teste: \"{!s}\" ele deveria dar erro!\n\n".format(str(data))
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
    text = os.linesep.join([s for s in text.splitlines() if s])
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
    acepeted_languages = ["python3","C++","C#"] # C# so funciona se um executavel ja existir

    json_file = read_git_url_json()


    for student in json_file:
        person = student["student_username"]
        
        
        if (not os.path.exists("reports/{!s}.txt".format(person))):
            print(person)
            error = test_main(test_dir,student)
            print("algum erro?: ",error)
            print("\n")