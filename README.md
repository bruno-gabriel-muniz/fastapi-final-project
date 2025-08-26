# fastapi-final-project

Este repositório contém meu projeto de finalização do curso [FastAPI do Zero](https://fastapidozero.dunossauro.com/estavel/15/), organizado pelo @dunossauro.

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

## 3. Progresso Atual

Sistema de usuário, romancistas, autenticação, docker e banco de dados funcionando.

Próximos passo: Aplicar o CRUD dos livros.

## 4. Como Rodar

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

## 5. Resultados

...