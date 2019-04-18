# MonitoriaLogComp
Repositorio de ferramentas de avaliacao de compiladores feitos na materia

## Como rodar:

1. copiar path do github dos compiladores dos alunos no arquivo git_paths.txt (ex: aluno1/compilador);
2. Para puxar a release x.x de cada um, basta usar, por exemplo:
```
$ ./get_releases.sh 2.2
```

Isso criara uma pasta da release x.x com uma pasta por aluno, contendo o compilador. Na pasta da release tambem havera um template para avaliacao por aluno,casos eja necessario submeter uma issue. Sarquivos de feedback criados nao serao substituidos;

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