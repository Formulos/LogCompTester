# Auto Tester

Instruções para o uso do servidor para correção automática de compiladores.

## Cadastro do webhook no servidor

### Instalação

Para configurar o servidor para ouvir aos webhooks:

- Clonar o repositório LogCompTester na máquina
- Instalar o apache2
- Em /etc/apache2/sites-enabled criar uma file chamada flask.conf
- Adicionar o seguinte código na file:

```
Listen 80
<VirtualHost *:80>

	ServerAdmin webmaster@localhost
	DocumentRoot /var/www/html

        LogLevel debug

        WSGIScriptAlias / /<path_ate_o_repositorio>/LogCompTester/Compilers/my_flask.wsgi
        WSGIDaemonProcess flask-api processes=5 threads=1 user=ubuntu group=ubuntu display-name=%{GROUP}
        WSGIProcessGroup flask-api
        WSGIApplicationGroup %{GLOBAL}
        WSGIPassAuthorization On
        WSGIChunkedRequest On
        ErrorLog ${APACHE_LOG_DIR}/error-80.log
        CustomLog ${APACHE_LOG_DIR}/access-80.log combined

        <Directory /<path_ate_o_repositorio>/LogCompTester/Compilers>
            <IfVersion >= 2.4>
                Require all granted
            </IfVersion>
            <IfVersion < 2.4>
                Order allow,deny
                Allow from all
            </IfVersion>
        </Directory>

</VirtualHost>
```

- Editar a seguinte linha em LogCompTester/Compilers/servidor.py :

```
BASE_DIR = '/<path_ate_o_repositorio>/LogCompTester/Compilers'
```
- Editar a seguinte linha em LogCompTester/Compilers/issuer_pusher.py :

```
token = "<github_token_do_monitor>"
```
- Editar a seguinte linha em LogCompTester/Compilers/my_flask.wsgi :

```
sys.path.insert(0, "/<path_ate_o_repositorio>/LogCompTester/Compilers")
```
- Adicionar a seguinte linha ao .bashrc :

```
export GITHUB_TOKEN="<github_token_do_monitor>"
```
- Restartar o servidor apache2
- Para testar se o servidor está rodando é possível acessar http://<ip_do_servidor>/ onde deve receber uma mensagem de "Hello World"

### Adicionando ao banco de dados

Editar o arquivo LogCompTester/Compilers/db/populate.sql

- Para inserir uma nova versão:

```
INSERT INTO version (version_name, direct_input, extension, date_from, date_to) VALUES(<version_name>, <1 (True) ou 0 (False)>, <extension>, <date_from>, <date_to>);
```

- Para inserir um novo aluno:

```
INSERT INTO users (git_username, name, surname) VALUES(<git_username>, <name>, <surname>);
```

- Para inserir um novo repositório:

```
INSERT INTO repository (git_username, repository_name, language, compiled, program_call) VALUES(<git_username>, <repository_name>, <language>, <1 (True) ou 0 (False)>, <program_call>);
```

Após editar o populate.sql, rodar o arquivo populate.py

### Logs

Logs do servidor podem ser acessadas em /var/log/apache2/access-80.log e /var/log/apache2/error-80.log

## Cadastro do webhook para o aluno

Para adicionar o corretor automático ao seu repositório, o aluno deve:

- Ir na aba Settings -> Webhooks -> Add Webhook
- Em "Payload URL" o aluno deve adicionar http://<ip_do_servidor>/webhook
- Em "Content Type" o aluno deve selecionar a opção application/json
- Em "Which events would you like to trigger this webhook?" o aluno deve selecionar "Let me select individual events" e em seguida marcar APENAS as opções "Branch or tag creation" e "Releases"
- Ao final deixar a opção "Active" ligada

OBS: A pessoa (monitor) que tiver com o seu GITHUB_TOKEN cadastrado no servidor deve ser adicionada como colaborador no repositório do aluno

## Imagem SVG dos resultados

### Adicionando o SVG ao README

Para adicionar a imagem svg dos resultados dos testes o aluno deve:

- Adicionar a seguinte chamada de API ao seu README.md:

```
![git_status](http://<ip_do_servidor>/svg/<Usuario_Github>/<Repositorio_Compilador>/)
```

### Legenda do SVG

Os possíveis valores para a coluna do meio são:

- **Delayed**: Quando o aluno falha em passar nos testes até o deadline de entrega da versão
- **On time**: Quando ainda há prazo até o deadline da versão ou se o aluno passou nos testes a tempo

Os possíveis valores para a terceira coluna são:

- **Error**: Quando ocorre algum erro ao executar os testes na release do aluno
- **Failed**: Quando o resultado dos testes é diferente do esperado
- **To do**: Quando você ainda não soltou nenhuma release da versão
- **Pass**: Quando passou em todos os testes

## Uso

O corretor é "acionado" quando uma release ou tag é criada pelo aluno
