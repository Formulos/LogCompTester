import os
import subprocess
import re

def auto_issue(name,text):
    #print(name)
    '''
    Existe um problema nisso, o subproces tem uma quantida maxima de argumentos e como o texto é um argumento
    pode acontecer de passar, isso só aconteceu uma vez com um reporte de 4483 linhas, então é dificil.
    Se continuar dando problema um jeito de arrumar é caso o texto ser muito longo dividir o txt em pedaços
    e passar eles como comentários.
    '''
    subprocess.run(["ghi", "open","-m","autoIssue\n"+text],cwd="src/{!s}".format(name))


if __name__ == '__main__':
    DIR = "reports/"
    file_list = ([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    for f in file_list:
        name = f[:-4] #tira o .txt

        with open("reports/{!s}".format(f), 'r') as file:
            text = file.read()

        auto_issue(name,text)