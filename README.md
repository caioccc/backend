# Backend para Todo List App - Selecao OPME

Backend para aplicação de Todo List App, desenvolvido em Python 3.10, com Django Framework, Django Rest Framework, Django Knox e PostgreSQL.

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)

[![Maintenance](https://img.shields.io/badge/Django-v4.2-%3CCOLOR%3E)](https://img.shields.io/badge/Django-v3.1.7-%3CCOLOR%3E)
[![Linux](https://svgshare.com/i/Zhy.svg)](https://svgshare.com/i/Zhy.svg)
[![Windows](https://svgshare.com/i/ZhY.svg)](https://svgshare.com/i/ZhY.svg)

## **Tabela de Conteúdos**

- [📝 Descrição](#descrição)
- [🚀 Instalação](#instalação)
- [Swagger](#swagger)
- [Testes](#testes)
- [Qualidade de código](#qualidade-de-código)
- [Endpoints](#endpoints)
- [Docker](#docker)
- [Licença](#licença)
- [Autor](#autor)

## 📝 Descrição

Este projeto foi desenvolvido em Python 3.10, com Django Framework, Django Rest Framework, Django Knox e PostgreSQL.

## Instalação

Para rodar este backend aplicação você deverá seguir os passos abaixo.
OBS: É necessário ter o Python 3.10 instalado.

1 - Instale as dependencias

```bash
  pip install -r requirements.txt
```

2 - Rode os comandos abaixo para criar o banco de dados e as tabelas

```bash
  python manage.py makemigrations
  python manage.py migrate
```

3 - Crie um super usuário para acessar o admin

```bash
  python manage.py createsuperuser
```

4 - Rode o servidor

```bash
  python manage.py runserver
```

## Swagger

![Swagger](https://i.imgur.com/dORtVmp.png)

Tomei a liberdade de incrementar ainda mais a qualidade de projeto backend adicionando mais uma camada para futuros desenvolvedores terem acesso a documentação da API, o Swagger.

A idéia é simplificar o desenvolvimento desta API pois esta ferramenta pode nos ajudar a projetar e documentar as APIs em escala.

Para acessar a documentação da API, acesse o link abaixo:

```bash
  http://localhost:8000/swagger/
```

Neste link será possível visualizar todos os endpoints disponíveis, bem como os métodos permitidos e os parâmetros necessários para cada endpoint.

## Testes

Todos os testes criados são testes de integração, pois não haveria necessidade de implementação de testes unitários
visto que o sistema ainda é pequeno, e todas as funções e métodos implementados são utilizados dentro dos testes de
integração, portanto, os comportamentos esperados de cada função são testados nestes testes de integração.

Para rodar os testes de integração implementados, basta executar o comando abaixo:

```bash
  python manage.py test
```

Uma suíte com 20 testes irá rodar. Você pode verificar o resultado no terminal. Os testes podem ser encontrados nas
respectivas pastas "tests" de cada módulo.

## Qualidade de código

Para verificar a qualidade de código, foi utilizado o Flake8, que é um linter de código.

Flake8 é uma biblioteca Python que envolve PyFlakes, pycodestyle e o script McCabe de Ned Batchelder. É um ótimo kit de
ferramentas para verificar sua base de código em relação ao estilo de codificação (PEP8), erros de programação (como
“biblioteca importada, mas não utilizada” e “nome indefinido”) e para verificar a complexidade ciclomática.

Para rodar o Flake8, basta
executar o comando abaixo:

```bash
  flake8
```

Erros mais comuns onde foram todos corrigidos com a utilização do Flake8:

- [x] E501 line too long (> 140 characters)
- [x] E231 missing whitespace after ','
- [x] E305 expected 2 blank lines after class or function definition, found 1
- [x] E303 too many blank lines
- [x] E261 at least two spaces before inline comment
- [x] E225 missing whitespace around operator
- [x] E128 continuation line under-indented for visual indent


## Endpoints

Para acessar todos os endpoints criados, é necessário estar logado no sistema, pois todos os endpoints utilizáveis
requer o token de autorização. Para isso, é necessário criar um usuário e fazer o login.

### Endpoints para Autenticação

- [x] POST /api/auth/register/

Cria um novo usuário. É necessário enviar o username, email e password.

  ``` json
    {
      "username": "caio",
      "email": "caio@gmail.com",
      "password": "Admin123!"
    } 
  ```

- [x] POST /api/auth/login/

Faz o login do usuário. Após o login você receberá um Token de autorização para você poder realizar as consultas neste
backend.
O Token deve ser enviado no cabeçalho no padrão:

```
Token <token_hash>
```

Os dados a serem enviados são:

``` json
  {
      "username": "caio",
      "password": "Admin123!"
    } 
```

- [x] POST /api/auth/logout/ - Faz o logout do usuário. Requer o Token de autorização.
- [x] GET /api/auth/user/ - Retorna os dados do usuário logado. Requer o Token de autorização.


## Docker
Além da instalação manual, o projeto também pode ser executado em um container Docker. Para isso, temos dois caminhos bem fáceis. Assim, basta seguir os passos abaixo:

### Primeiro caminho

Com o docker e docker-compose instalados, basta rodar o comando abaixo na raiz do projeto backend:

```bash
  docker-compose up --build
```

A aplicação já estará rodando em http://localhost:8000


### Segundo caminho

1 - Crie a imagem do projeto

```bash
  docker build -t backend .
```

2 - Rode o container

```bash
  docker run -p 8000:8000 backend
```

3 - Acesse o endereço do backend:

```bash
  http://localhost:8000/
```


## 📝 Licença

Este projeto esta sobe a licença [MIT](./LICENSE).

## Autor

<a href="#">
 <img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/7137962?v=4" width="100px;" alt=""/>
</a>
 <br />
 <sub><b>Caio Marinho</b></sub>
 <a href="#" title="Caio Marinho">🚀</a>

[![Linkedin Badge](https://img.shields.io/badge/-Caio%20Marinho-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/caiomarinho/)](https://www.linkedin.com/in/caiomarinho/)
[![Gmail Badge](https://img.shields.io/badge/-caiomarinho8@gmail.com-c14438?style=flat-square&logo=Gmail&logoColor=white&link=mailto:caiomarinho8@gmail.com)](mailto:caiomarinho8@gmail.com)

Made with ❤️ by [Caio Marinho!](https://caiomarinho.tech/) 👋🏽 [Get in Touch!](https://www.linkedin.com/in/caiomarinho/)
