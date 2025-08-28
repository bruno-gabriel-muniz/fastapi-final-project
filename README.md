![Top Language](https://img.shields.io/github/languages/top/bruno-gabriel-muniz/fastapi-final-project)
![Build](https://github.com/bruno-gabriel-muniz/fastapi-final-project/actions/workflows/ci.yaml/badge.svg)
[![codecov](https://codecov.io/gh/bruno-gabriel-muniz/fastapi-final-project/branch/main/graph/badge.svg)](https://codecov.io/gh/bruno-gabriel-muniz/fastapi-final-project)


# fastapi-final-project

Este repositório contém meu projeto de finalização do curso [FastAPI do Zero](https://fastapidozero.dunossauro.com/estavel/15/), organizado pelo @dunossauro.

## Sumário:

- [0. Minha Experiência Com o Curso](#0-minha-experiência-com-o-curso)
- [1. Contexto](#1-contexto)
- [2. Decisões](#2-decisões)
- [3. Como Rodar](#3-como-rodar)
- [4. Resultados](#4-resultados)

## 0. Minha Experiência Com o Curso

Excelente curso!

Foi divertido acompanhar as aulas e a minha evolução ao lidar com meus erros no processo e no final perceber uma grande melhoria nas minhas habilidades técnicas e na minha maturidade.

E é claro, isso só foi possível graças ao excelente conteúdo e didática do Dunossauro.

## 1. Contexto

O curso tem como objetivo ensinar o básico de FastAPI e usar este conhecimento como contexto para ensinar outras habilidades de desenvolvimento web.

- Testes automatizados (pytest);
- SQLAlchemy;
- Migração de Banco de Dados (Alembic);
- Segurança;
- Código Assíncrono;
- Docker; e
- Integração contínua.

## 2. Decisões

### 2.1. Escolha do FastAPI

Escolhido devido a facilidade de uso, eficiência e validação automática de dados.

### 2.2. Outras Bibliotecas utilizadas

- pytest e pytest-cov para testes automatizados e cobertura de testes;
- SQLAlchemy para ORM;
- Alembic para migração de banco de dados;
- Passlib e pyjwt para hash de senhas e validação de tokens JWT;
- loguru para logging;
- Docker para containerização; e
- GitHub Actions para integração contínua.

### 2.3. Estrutura do Projeto

A estrutura do projeto foi feita em uma unica camada devido a simplicidade e falta de um Front-end.

Pastas:
```
├── migrations
│
├── src
│   ├── __init__.py
│   └── tcc_madrs
│       ├── app.py
│       ├── database.py
│       ├── __init__.py
│       ├── models.py
│       ├── routers
│       │   ├── books.py
│       │   ├── novelist.py
│       │   └── users.py
│       ├── sanitize.py
│       ├── schemas.py
│       ├── security.py
│       └── settings.py
└── tests
    ├── conftest.py
    ├── __init__.py
    ├── test_app.py
    ├── test_books.py
    ├── test_conta.py
    ├── test_db.py
    └── test_novelist.py

```

## 3. Como Rodar


### 3.1. Variáveis do Settings

As variáveis de ambiente necessárias para o funcionamento do projeto estão no arquivo `.env`. Um exemplo de configuração é:

```
DATABASE_URL_UPDATE="postgresql+psycopg://app_user:app_password@127.0.0.1:5432/app_db"
DATABASE_URL="postgresql+psycopg://app_user:app_password@madrs_database:5432/app_db"
SECRET_KEY=your_secret_key
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60
```

### 3.2. Comandos e Requisitos
Para rodar o projeto, é necessário ter o Poetry instalado. Além disso, siga os seguintes passos:

1. Clone o repositório:
   ```
   git clone https://github.com/seu_usuario/fastapi-final-project.git
   cd fastapi-final-project
   ```

2. Inicie o ambiente Poetry:
   ```
   poetry install
   ```

3. Entre nele:
   ```
   poetry shell
   ```

4. Rode os testes com:
   ```
   task test
   ```

5. Execute a API com:
   ```
   task run
   ```

## 4. Resultados

Consegui ter uma boa experiência prática, ao aprender a usar o FastAPI e outras ferramentas de desenvolvimento.

Assim como, consegui manter um bom ritmo de estudos e implementações, fazendo, cumprindo e replanejando prazos, conforme o necessário, para entregar o projeto em 2 semanas.

Assim sendo, estou satisfeito com o resultado final e ansioso para aplicar o que aprendi em projetos futuros.