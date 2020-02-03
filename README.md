# MonitoriaLogComp
Repositorio de ferramentas de avaliacao de compiladores feitos na materia

## Como rodar:

0. Instalar python (versão 3.7 ou acima) e a dependência gitPython:
```
$ pip install gitpython
```

1. copiar path do github dos compiladores dos alunos em um arquivo json;
2. Para puxar a release x.x de cada um, basta usar, por exemplo:
```
$ python fetch_releases.py git_paths.json 2.0
```

Isso criara uma pasta da release src/x.x com uma pasta por aluno, contendo o codigo fonte de compilador.

3. Para rodar testes de input de string no terminal, use, por exemplo:
```
$./run_test_lines.sh 1.2-tests.txt 1.2/aluno1/   
```

4. Para rodar testes de input de arquivos no terminal, use, por exemplo:
```
$./run_test_files.sh 2.0-tests/ 2.0/aluno1/   
```

Assume-se que o aluno possui um arquivo main.py no diretorio raiz de seu compilador. 

Se o aluno nao deu o release ou errou a tag da release, seu template de review devera estar vazio




versão 2.0 - Essa parte esta incompleta

o ghi esta impedindo o projeto de ser realmente automatico ja que precisa configurar ele, e ele não suporta uma chave ssh

installar ghi
gem install ghi

parece que funciona com pip mas não tenho certeza

ghi config --auth "username"

