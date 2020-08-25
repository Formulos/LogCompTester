# MonitoriaLogComp
Repositório de ferramentas de avaliação de compiladores feitos na materia


## Dependências:


Existem duas dependências além do python

1. Gitpython usado para fazer o pull, ele pode ser instalado com:

```
$ pip install gitpython
```

2. Ghi usado para criar as issues ele precisa ser instalado e configurado:
```
$ sudo apt install ghi
$ ghi config --auth "username"
```
## Configurando projeto:

O codigo esta divido em três partes, fetch_releases.py, auto_test.py e issuer_pusher.py elas em ordem fazem pull de todos os repositórios, fazem todos os testes para os repositórios e criam as issues.

O fetch_releases precisa de uma chave SSH configurada para se comunicar com o github é esperado que ela esteja no path "~/.ssh/id_rsa" que é o padrão.
Um tutorial de como criar uma chave ssh para o github pode ser encontrado [aqui](https://help.github.com/en/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

Tanto o fetch_releases e o auto_test precisam de um git_paths configurado, o git_paths.json contém uma lista de dicionários com as informações de todos os alunos,
ele tem os seguintes parâmetros:
1. student_username - nome do usuario git do aluno
2. repository_name - nome do repositorio que contem o compilador
3. run_args - é os argumentos que um cmd precisa para executar o compilador
4. compile_args - é os argumentos que um cmd precisa para compilar o compilador, so é necessário se linguagem precisar de compilação
5. language - é a língua que o compilador está escrita

Um exemplo pode ser visto a seguir:

```
[
    {
        "student_username": "lucassa3",
        "repository_name" : "compilador",
        "run_args" : "python3 somador.py",
	"language" : "python3"
    },
    {
        "student_username": "raulikeda",
        "repository_name" : "rep",
        "run_args" : "./out/compylador",
        "compile_args": "dotnet build --nologo -o out",
	"language" : "C#"
    }
]
```

## Como rodar:

Importante: todos os caminhos do código estão relativos, assim eles os programas precisam ser executados por um cmd que está dentro da pasta Compiler

Ao executar o fetch_releases ele deleta todos os reports e os codigos dos alunos que estão em src
1. Para puxar a release x.x de cada aluno, basta usar:
```
$ python fetch_releases.py git_paths.json 2.0
```
Se uma release não for encontrada é criado um report dentro da pasta reports

2. Para rodar o os testes para todos os alunos
```
$ python3 auto_test.py php/2.4
```
Como o auto_test somente chama um subprocess para executar o código, o computador utilizado precisa ser capaz de compilar e executar o código.

O auto_testes executa os testes para todos os alunos que não tem um report na pasta de reports.

O auto_testes tambem tem algumas constantes no começo do código, elas são:
1. acepeted_languages - lista das linguagem que esse programa foi testado com, se uma linguagem não estiver e estiver no json um erro é gerado.
2. compile_languages - lista as linguagens que precisam de uma etapa de compilação antes da execução.
3. maxtime - tempo maximo que cada teste deve rodar antes de dar um timeout em segundos (é um float).
4. direct_input -(True ou False) diz se é passado o conteúdo de um teste, em vez do caminho dele, é usado para as versões baixas.
5. assembly - (True ou False) usado para testar a versão assembly, somente roda o arquivo de teste para cada aluno, e mostra um erro no terminal se ouve um erro na execução do teste, ele não gera reports automáticos.
6. assembly_test - o número do teste de assembly, geralmente só vai ter 1, é usado somente se assembly = True.

para executar o issuer_pusher.py é só necessário rodar:
```
python3 issuer_pusher.py
```
Ele pega o conteúdo de todos os reports e cria uma issue com o nome autoIssue para cada aluno, se um report não existe não é criado uma issue para o aluno.
É um código simples que somente chama o ghi na pasta src/aluno e passa como stdin o conteúdo de report.


## Criando novos testes:

Todos os testes devem estar dentro da pasta tests e devem estar organizados por versão, o auto_test irá executar todos os testes da pasta especificada, porém ele não podem pular um número (ou seja não deve existir teste2.php sem teste1.php). Para um teste ser executado ele precisa de um teste{x}.php (ou .txt nos testes das versões baixos) que contem contem o código que deve ser testado, também precisa de um sol{x}.txt que contém a solução do teste correspondente, a solução deve ser exatamente o que o print do compilador deve gerar (cuidado com \n), ou seja precisa ter um número par de arquivos e todo o teste precisa ter um sol correspondente. Se o teste for feito para gerar um erro a solução correspondente deve conter somente a string "Error" qualquer outro conteúdo (incluindo \n) e o teste não é considerado um teste de erro.

Também é possível gerar um teste que recebe um input, nesse caso é preciso criar um outro arquivo dentro da pasta inputs que deve estar dentro da pasta {X}_tests , ele deve se chamar input{x}.txt sendo que x deve ser o número do teste que deve receber o input, diferente dos testes que não podem pular um número, os inputs podem. Pode ser criado mais de um input para um teste, para isso necessário usar um \n dentro do input{x}.txt, como exemplo, no input abaixo o 4 e o 2 são passados como inputs diferentes (ou seja cada linha do input{x}.txt é um input novo).
```
4
2
```
Cuidado com \n se eles existirem como primeira linha input{x}.txt é mandado algo vazio para o stdin provavelmente gerando um teste diferente do esperado.

Usei um código simples que esta dentro de util chamdo simple_test_maker.py para ajudar na criação de novos testes.
