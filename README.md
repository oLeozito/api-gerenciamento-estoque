# API de Gerenciamento de Estoque - 愚公移山 Variedades

API RESTful desenvolvida para a centralização, gestão e auditoria do estoque da loja de produtos importados **愚公移山 Variedades**, no âmbito do Desafio Técnico da Trilha Back-End (Processo Seletivo Ecomp Jr. 2026.2 - UEFS).

---

## Sumario

1. [Contexto e Problema](#contexto-e-problema)
2. [Tecnologias e Ferramentas](#tecnologias-e-ferramentas)
3. [Arquitetura e Estrutura de Pastas](#arquitetura-e-estrutura-de-pastas)
4. [Mecanismos de Seguranca e Regras de Negocio](#mecanismos-de-seguranca-e-regras-de-negocio)
5. [Como Rodar o Projeto com Docker](#como-rodar-o-projeto-com-docker)
6. [Documentacao Detalhada das Rotas](#documentacao-detalhada-das-rotas)
   - [Autenticacao e Usuarios (/auth)](#1-autenticacao-e-usuarios-auth)
   - [Categorias (/categorias)](#2-categorias-categorias)
   - [Fornecedores (/fornecedores)](#3-fornecedores-fornecedores)
   - [Produtos (/produtos)](#4-produtos-produtos)
   - [Movimentacoes (/movimentacoes)](#5-movimentacoes-movimentacoes)
   - [Dashboard Estrategico (/dashboard)](#6-dashboard-estrategico-dashboard)
7. [Consultas Avancadas e Inteligencia de Negocio](#consultas-avancadas-e-inteligencia-de-negocio)
8. [Padroes de Commit e Codigo](#padroes-de-commit-e-codigo)

---

## Contexto e Problema

A **愚公移山 Variedades** operava seu controle de inventario de forma puramente manuscrita. Essa abordagem gerava limitacoes severas na operacao:
- Impossibilidade de correlacionar produtos a seus respectivos fornecedores e categorias de modo confiavel;
- Ausencia de historico confiavel e rastreavel de entradas e saidas de mercadorias;
- Vulnerabilidade a discrepancias de saldo fisico versus saldo registrado;
- Dificuldade para planejar compras, reabastecimentos e identificar itens com estoque critico.

A presente solucao disponibiliza uma API robusta e padronizada que serve como nucleo confiavel para organizar cadastros relacionais, aplicar regras de negocio transacionais na movimentacao de estoque e servir como base para interfaces web ou mobile.

---

## Tecnologias e Ferramentas

- **Python 3.11:** Linguagem base, com recursos modernos de tipagem estatica.
- **FastAPI:** Framework web moderno de alto desempenho, com geracao automatica de schemas OpenAPI e validacao transparente.
- **PostgreSQL 15:** SGBD relacional responsavel por assegurar consistencia ACID, integridade referencial e constraints de banco de dados.
- **SQLAlchemy 2.0:** ORM declarativo utilizado para mapeamento das entidades relacionais, sessoes transacionais e consultas analiticas.
- **Alembic:** Ferramenta para versionamento e migracao incremental do schema do banco de dados.
- **Pydantic v2 & Pydantic-Settings:** Validacao estrita de dados de entrada/saida (Data Transfer Objects) e gerenciamento seguro de configuracoes de ambiente.
- **PyJWT:** Emissao e decodificacao de tokens de acesso stateless (Bearer Token).
- **Passlib & Bcrypt:** Funcoes de derivacao de chave (hashing) unidirecional com salt aleatorio para proteger senhas.
- **Docker & Docker Compose:** Empacotamento de aplicacao e banco de dados em containers isolados, garantindo reprodutibilidade em qualquer ambiente.
- **Uvicorn:** Servidor ASGI de nivel de producao.
- **Makefile:** Automacao de comandos operacionais frequentes.

---

## Arquitetura e Estrutura de Pastas

O projeto adota os principios da **Clean Architecture**, isolando responsabilidades tecnicas e regras de negocio em camadas bem delineadas:

```text
app/
├── api/             # Camada de apresentacao (controladores de rotas e dependencias)
│   ├── auth/        # Endpoints de autenticacao e gestao de usuarios
│   ├── categoria/   # Endpoints de categorias
│   ├── dashboard/   # Endpoints analiticos e metricas consolidadas
│   ├── fornecedor/  # Endpoints de fornecedores
│   ├── movimentacao/# Endpoints de movimentacoes de estoque
│   ├── produto/     # Endpoints de catalogo de produtos
│   └── deps.py      # Injecao de dependencias (sessao de banco, validacao JWT e RBAC)
├── core/            # Configuracoes centrais do sistema
│   ├── config.py    # Leitura tipada de variaveis de ambiente (.env)
│   ├── database.py  # Engine do SQLAlchemy e factory de sessoes (get_db)
│   └── security.py  # Funcoes criptograficas (hashing de senha e geracao de JWT)
├── enums/           # Enumeracoes com tipagem estrita
│   ├── cargo.py     # Niveis hierarquicos de acesso (admin, gerente, estoquista)
│   └── tipo_movimentacao.py # Tipos validos de movimentacao (ENTRADA, SAIDA)
├── models/          # Entidades persistentes do SQLAlchemy (tabelas e relacionamentos)
│   ├── base.py      # DeclarativeBase do SQLAlchemy
│   ├── mixins.py    # Mixins reutilizaveis (ex: controle de created_at e updated_at)
│   ├── categoria.py # Mapeamento da tabela categorias
│   ├── fornecedor.py# Mapeamento da tabela fornecedores
│   ├── movimentacao.py # Mapeamento da tabela movimentacoes
│   ├── produto.py   # Mapeamento da tabela produtos
│   └── usuario.py   # Mapeamento da tabela usuarios
├── repositories/    # Camada de persistencia e acesso a dados (consultas isoladas)
│   ├── categoria_repository.py
│   ├── fornecedor_repository.py
│   ├── movimentacao_repository.py
│   ├── produto_repository.py
│   └── usuario_repository.py
├── schemas/         # Contratos Pydantic de entrada e saida (DTOs)
│   ├── categoria.py
│   ├── dashboard.py
│   ├── fornecedor.py
│   ├── movimentacao.py
│   ├── produto.py
│   ├── token.py
│   └── usuario.py
├── scripts/         # Utilitarios de manutencao operacional
│   └── create_admin.py # Criacao do primeiro usuario administrador via CLI
├── services/        # Regras de negocio puras e orquestracao de transacoes
│   ├── auth_service.py
│   ├── categoria_service.py
│   ├── dashboard_service.py
│   ├── fornecedor_service.py
│   ├── movimentacao_service.py
│   ├── produto_service.py
│   └── usuario_service.py
├── utils/           # Funcoes utilitarias transversais
└── main.py          # Ponto de entrada do FastAPI
```

---

## Mecanismos de Seguranca e Regras de Negocio

### 1. Autenticacao Stateless com JWT
- A autenticacao utiliza tokens no formato JSON Web Token assinados com o algoritmo HMAC-SHA256 (`HS256`).
- As rotas protegidas validam o token via `HTTPBearer` no header `Authorization: Bearer <token>`.
- O payload armazena o identificador unico do usuario (`sub`) e o cargo correspondente (`role`).

### 2. Controle de Acesso Baseado em Papeis (RBAC)
O sistema implementa tres niveis de perfil com granularidade de operacoes:
- **`admin`:** Acesso irrestrito a todas as operacoes, incluindo exclusao fisica (`DELETE`) de registros e criacao de contas com qualquer nivel de permissao.
- **`gerente`:** Pode consultar dados, cadastrar e alterar produtos, categorias e fornecedores, alem de visualizar o dashboard. Pode cadastrar novos usuarios estritamente com perfil `estoquista`. Nao possui autorizacao para exclusoes (`DELETE`).
- **`estoquista`:** Foco operacional. Pode consultar produtos, categorias e fornecedores para suporte ao inventario, e possui permissao para lancar movimentacoes de entrada e saida. Nao pode cadastrar produtos, categorias ou fornecedores nem acessar o painel de gestao de usuarios/dashboard.

### 3. Imutabilidade do Historico de Auditoria
- As movimentacoes de estoque sao **imutaveis**. Uma vez registradas, nao podem ser alteradas (`PUT`/`PATCH`) nem excluidas (`DELETE`) pela API.
- A exclusao fisica de produtos com movimentacoes associadas e bloqueada pelo banco de dados atraves da restricao de chave estrangeira com `ON DELETE RESTRICT`, garantindo a integridade do historico contabil e de auditoria.

### 4. Transacoes Atomicas e Consistencia de Saldo
- Ao registrar uma movimentacao de estoque:
  - Para movimentacoes de **SAIDA**: valida-se previamente se a quantidade solicitada nao excede o saldo atual em estoque. Em caso de insuficiencia, a operacao é rejeitada com codigo HTTP `400 Bad Request`. Havendo saldo, a deducao ocorre na mesma transacao.
  - Para movimentacoes de **ENTRADA**: o saldo do produto é incrementado e, caso informado o valor unitario, o preco de custo de referencia é atualizado.
  - Tanto o registro da movimentacao quanto a atualizacao da quantidade do produto sao persistidos na mesma sessao de banco de dados (`commit` unico), prevenindo divergencias entre a tabela de movimentacoes e a de produtos.

### 5. Tratamento Padronizado de Erros e Protecao de Dados Internos
- Respostas de falha utilizam codigos de status HTTP semanticamente corretos:
  - `400 Bad Request`: violacoes de regras de negocio (ex: saldo insuficiente, tentativa de excluir produto com movimentacoes).
  - `401 Unauthorized`: credenciais ausentes, invalidas ou token expirado.
  - `403 Forbidden`: usuario autenticado porem sem o cargo necessario para a operacao.
  - `404 Not Found`: recurso solicitado nao localizado por identificador.
  - `409 Conflict`: duplicidade de campos unicos (ex: SKU/codigo de produto, CNPJ ou e-mail de fornecedor, nome de categoria, nome de usuario).
  - `422 Unprocessable Entity`: falha de formato, tipo ou referencia inexistente de chaves estrangeiras.
- Detalhes internos de infraestrutura, logs de conexao ou stack traces nao sao expostos ao cliente final.

---

## Como Rodar o Projeto com Docker

### Pre-requisitos
- Docker (versao 20.10 ou superior)
- Docker Compose (versao 2.0 ou superior)
- Make (opcional, para uso de atalhos)

### Passo 1: Clonar o Repositorio
```bash
git clone https://github.com/oLeozito/api-gerenciamento-estoque.git
cd api-gerenciamento-estoque
```

### Passo 2: Configurar as Variaveis de Ambiente
Copie o arquivo de exemplo e ajuste as credenciais desejadas:
```bash
cp .env.example .env
```

Conteudo padrao do `.env`:
```env
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=erp_db

DATABASE_URL=postgresql://postgres:postgres@db:5432/erp_db

SECRET_KEY=uma_chave_super_secreta_qualquer_para_rodar_local
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

ADMIN_NOME=Administrador
ADMIN_USER=admin
ADMIN_SENHA=admin123
```

### Passo 3: Subir os Containers
Execute o build e a inicializacao dos servicos via Docker Compose:
```bash
docker compose up -d --build
```
Isso inicializara:
- O banco de dados PostgreSQL na porta `5432`.
- A API FastAPI na porta `8000`.

### Passo 4: Aplicar as Migracoes do Banco de Dados (Alembic)
Com os containers ativos, execute as migracoes para criar todas as tabelas e constraints:
```bash
docker compose exec api alembic upgrade head
```

### Passo 5: Criar o Usuario Administrador Inicial
Para registrar o primeiro usuario administrador no banco de dados (conforme configurado nas variaveis `ADMIN_*` do `.env`):
```bash
make create-admin
```
Ou diretamente via Docker:
```bash
docker compose exec api python -m app.scripts.create_admin
```

### Passo 6: Acessar a Documentacao Interativa
Apos a inicializacao, a documentacao automatica gerada pelo FastAPI estara disponivel em:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

## Documentacao Detalhada das Rotas

### Matriz de Permissoes por Modulo

| Modulo | Endpoint | Metodo | Publico | Estoquista | Gerente | Admin |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Auth** | `/auth/login` | POST | Sim | Sim | Sim | Sim |
| **Auth** | `/auth/usuarios` | POST | Nao | Nao | Sim (apenas estoquistas) | Sim (qualquer cargo) |
| **Categorias** | `/categorias` | GET | Nao | Sim | Sim | Sim |
| **Categorias** | `/categorias` | POST | Nao | Nao | Sim | Sim |
| **Categorias** | `/categorias/{id}` | PATCH | Nao | Nao | Sim | Sim |
| **Categorias** | `/categorias/{id}` | DELETE | Nao | Nao | Nao | Sim |
| **Fornecedores** | `/fornecedores` | GET | Nao | Sim | Sim | Sim |
| **Fornecedores** | `/fornecedores/{id}` | GET | Nao | Sim | Sim | Sim |
| **Fornecedores** | `/fornecedores` | POST | Nao | Nao | Sim | Sim |
| **Fornecedores** | `/fornecedores/{id}` | PATCH | Nao | Nao | Sim | Sim |
| **Fornecedores** | `/fornecedores/{id}` | DELETE | Nao | Nao | Nao | Sim |
| **Produtos** | `/produtos` | GET | Nao | Sim | Sim | Sim |
| **Produtos** | `/produtos/alerta-estoque` | GET | Nao | Sim | Sim | Sim |
| **Produtos** | `/produtos/{id}` | GET | Nao | Sim | Sim | Sim |
| **Produtos** | `/produtos` | POST | Nao | Nao | Sim | Sim |
| **Produtos** | `/produtos/{id}` | PATCH | Nao | Nao | Sim | Sim |
| **Produtos** | `/produtos/{id}` | DELETE | Nao | Nao | Nao | Sim |
| **Movimentacoes** | `/movimentacoes` | GET | Nao | Sim | Sim | Sim |
| **Movimentacoes** | `/movimentacoes/produto/{produto_id}` | GET | Nao | Sim | Sim | Sim |
| **Movimentacoes** | `/movimentacoes` | POST | Nao | Sim | Sim | Sim |
| **Dashboard** | `/dashboard` | GET | Nao | Nao | Sim | Sim |

---

### 1. Autenticacao e Usuarios (`/auth`)

#### `POST /auth/login`
Autentica o usuario e retorna o token de acesso Bearer JWT.

- **Acesso:** Publico.
- **Corpo da Requisicao (`application/json`):**
```json
{
  "usuario": "admin",
  "senha": "admin123"
}
```
- **Resposta de Sucesso (`200 OK`):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
  "token_type": "bearer"
}
```
- **Respostas de Erro:**
  - `401 Unauthorized`: Usuario ou senha incorretos.

#### `POST /auth/usuarios`
Cadastra um novo usuario do sistema.

- **Acesso:** `admin` (pode criar admin, gerente e estoquista) ou `gerente` (pode criar apenas estoquista).
- **Header:** `Authorization: Bearer <token>`
- **Corpo da Requisicao (`application/json`):**
```json
{
  "nome": "Carlos Silva",
  "usuario": "carlos.estoque",
  "senha": "senhaSegura123",
  "cargo": "estoquista"
}
```
- **Resposta de Sucesso (`201 Created`):**
```json
{
  "id": "e6f4776c-fb9e-473d-9d41-3b7c845ad35e",
  "nome": "Carlos Silva",
  "usuario": "carlos.estoque",
  "cargo": "estoquista",
  "created_at": "2026-10-25T10:00:00Z"
}
```
- **Respostas de Erro:**
  - `403 Forbidden`: Gerente tentando cadastrar usuario com perfil admin ou gerente.
  - `409 Conflict`: Nome de usuario ja em uso.

---

### 2. Categorias (`/categorias`)

#### `GET /categorias`
Lista todas as categorias cadastradas.

- **Acesso:** Autenticado (`admin`, `gerente`, `estoquista`).
- **Resposta de Sucesso (`200 OK`):**
```json
[
  {
    "id": "92f3e8f8-bcf6-4449-8d14-3a6d71b3e941",
    "nome": "Eletronicos"
  }
]
```

#### `POST /categorias`
Cadastra uma nova categoria. O nome deve ser unico.

- **Acesso:** `admin`, `gerente`.
- **Corpo da Requisicao (`application/json`):**
```json
{
  "nome": "Utensilios Domesticos"
}
```
- **Resposta de Sucesso (`201 Created`):**
```json
{
  "id": "c138d6d6-fcf9-42b7-832f-45b0a70823da",
  "nome": "Utensilios Domesticos"
}
```
- **Respostas de Erro:**
  - `409 Conflict`: Categoria com este nome ja existente.

#### `PATCH /categorias/{id}`
Atualiza os dados de uma categoria existente.

- **Acesso:** `admin`, `gerente`.
- **Corpo da Requisicao (`application/json`):**
```json
{
  "nome": "Utensilios de Cozinha"
}
```
- **Resposta de Sucesso (`200 OK`):**
```json
{
  "id": "c138d6d6-fcf9-42b7-832f-45b0a70823da",
  "nome": "Utensilios de Cozinha"
}
```
- **Respostas de Erro:**
  - `404 Not Found`: Categoria nao encontrada.
  - `409 Conflict`: Novo nome coincide com categoria ja cadastrada.

#### `DELETE /categorias/{id}`
Remove fisicamente uma categoria.

- **Acesso:** Exclusivo `admin`.
- **Resposta de Sucesso (`204 No Content`):** Vazio.
- **Respostas de Erro:**
  - `404 Not Found`: Categoria inexistente.
  - `400 Bad Request`: Categoria possui produtos vinculados (restricao referencial).

---

### 3. Fornecedores (`/fornecedores`)

#### `GET /fornecedores`
Retorna listagem resumida de fornecedores.

- **Acesso:** Autenticado (`admin`, `gerente`, `estoquista`).
- **Resposta de Sucesso (`200 OK`):**
```json
[
  {
    "id": "67a998bb-4c28-44d5-a827-0466be937b25",
    "nome": "Importadora Oriente Ltda",
    "cnpj": "12345678000199"
  }
]
```

#### `GET /fornecedores/{id}`
Retorna os dados detalhados de um fornecedor especifico.

- **Acesso:** Autenticado (`admin`, `gerente`, `estoquista`).
- **Resposta de Sucesso (`200 OK`):**
```json
{
  "id": "67a998bb-4c28-44d5-a827-0466be937b25",
  "nome": "Importadora Oriente Ltda",
  "cnpj": "12345678000199",
  "telefone": "7531618354",
  "email": "contato@orienteimport.com"
}
```
- **Respostas de Erro:**
  - `404 Not Found`: Fornecedor nao encontrado.

#### `POST /fornecedores`
Cadastra um fornecedor. CNPJ e e-mail devem ser unicos.

- **Acesso:** `admin`, `gerente`.
- **Corpo da Requisicao (`application/json`):**
```json
{
  "nome": "Silk Road Distribuidora",
  "cnpj": "98765432000188",
  "telefone": "71999998888",
  "email": "vendas@silkroad.com"
}
```
- **Resposta de Sucesso (`201 Created`):**
```json
{
  "id": "4bfe9460-15cb-42bb-9273-04bc99cbde07",
  "nome": "Silk Road Distribuidora",
  "cnpj": "98765432000188",
  "telefone": "71999998888",
  "email": "vendas@silkroad.com"
}
```
- **Respostas de Erro:**
  - `409 Conflict`: CNPJ ou e-mail ja registrado no sistema.

#### `PATCH /fornecedores/{id}`
Atualiza campos de um fornecedor cadastrado.

- **Acesso:** `admin`, `gerente`.
- **Corpo da Requisicao (`application/json`):**
```json
{
  "telefone": "71988887777"
}
```
- **Resposta de Sucesso (`200 OK`):** Objeto do fornecedor atualizado.
- **Respostas de Erro:**
  - `404 Not Found`: Fornecedor nao localizado.
  - `409 Conflict`: Novo CNPJ ou e-mail ja pertence a outro registro.

#### `DELETE /fornecedores/{id}`
Remove um fornecedor.

- **Acesso:** Exclusivo `admin`.
- **Resposta de Sucesso (`204 No Content`):** Vazio.
- **Respostas de Erro:**
  - `404 Not Found`: Fornecedor inexistente.
  - `400 Bad Request`: Fornecedor vinculado a produtos existentes.

---

### 4. Produtos (`/produtos`)

#### `GET /produtos`
Lista os produtos cadastrados de forma simplificada.

- **Acesso:** Autenticado (`admin`, `gerente`, `estoquista`).
- **Resposta de Sucesso (`200 OK`):**
```json
[
  {
    "id": "e9fbaf3b-a827-4a0b-85d7-386d63ff4be9",
    "codigo": "PRD-LUMINARIA-01",
    "nome": "Luminaria LED Dobravel",
    "descricao": "Luminaria de mesa recarregavel USB",
    "qtd_estoque": 25
  }
]
```

#### `GET /produtos/alerta-estoque`
Consulta avancada que retorna produtos cujo saldo de estoque esta igual ou inferior ao limite estabelecido.

- **Acesso:** Autenticado (`admin`, `gerente`, `estoquista`).
- **Parametros de Query:** `limite` (inteiro, padrao: 10).
- **Resposta de Sucesso (`200 OK`):** Lista ordenada de forma ascendente pela quantidade em estoque.
```json
[
  {
    "id": "e9fbaf3b-a827-4a0b-85d7-386d63ff4be9",
    "codigo": "PRD-CABO-C",
    "nome": "Cabo USB-C Trancado 2m",
    "descricao": "Cabo de carregamento rapido",
    "qtd_estoque": 3
  }
]
```

#### `GET /produtos/{id}`
Retorna a ficha tecnica completa do produto, incluindo referencias de categoria, fornecedor e precos.

- **Acesso:** Autenticado (`admin`, `gerente`, `estoquista`).
- **Resposta de Sucesso (`200 OK`):**
```json
{
  "id": "e9fbaf3b-a827-4a0b-85d7-386d63ff4be9",
  "codigo": "PRD-LUMINARIA-01",
  "nome": "Luminaria LED Dobravel",
  "descricao": "Luminaria de mesa recarregavel USB",
  "preco_custo": 18.50,
  "preco_venda": 45.00,
  "categoria_id": "c138d6d6-fcf9-42b7-832f-45b0a70823da",
  "fornecedor_id": "4bfe9460-15cb-42bb-9273-04bc99cbde07",
  "qtd_estoque": 25
}
```
- **Respostas de Erro:**
  - `404 Not Found`: Produto nao encontrado.

#### `POST /produtos`
Cadastra um novo produto. O estoque inicial e fixado automaticamente em 0 (o saldo so deve ser alterado mediante movimentacao oficial). O codigo/SKU deve ser unico.

- **Acesso:** `admin`, `gerente`.
- **Corpo da Requisicao (`application/json`):**
```json
{
  "nome": "Fone de Ouvido Bluetooth Sem Fio",
  "codigo": "PRD-AUDIO-BT01",
  "descricao": "Fone intra-auricular com estojo carregador",
  "preco_custo": 35.00,
  "preco_venda": 89.90,
  "categoria_id": "c138d6d6-fcf9-42b7-832f-45b0a70823da",
  "fornecedor_id": "4bfe9460-15cb-42bb-9273-04bc99cbde07"
}
```
- **Resposta de Sucesso (`201 Created`):** Objeto detalhado do produto com `qtd_estoque: 0`.
- **Respostas de Erro:**
  - `409 Conflict`: Codigo/SKU informado ja pertence a outro produto.
  - `422 Unprocessable Entity`: `categoria_id` ou `fornecedor_id` invalidos/inexistentes.

#### `PATCH /produtos/{id}`
Atualiza dados cadastrais do produto.

- **Acesso:** `admin`, `gerente`.
- **Corpo da Requisicao (`application/json`):**
```json
{
  "preco_venda": 95.00
}
```
- **Resposta de Sucesso (`200 OK`):** Objeto detalhado com as alteracoes aplicadas.
- **Respostas de Erro:**
  - `404 Not Found`: Produto inexistente.
  - `409 Conflict`: Novo codigo/SKU ja em uso.
  - `422 Unprocessable Entity`: Categoria ou fornecedor referenciados invalidos.

#### `DELETE /produtos/{id}`
Exclui um produto do catalogo.

- **Acesso:** Exclusivo `admin`.
- **Resposta de Sucesso (`204 No Content`):** Vazio.
- **Respostas de Erro:**
  - `404 Not Found`: Produto nao encontrado.
  - `400 Bad Request`: Nao e possivel excluir produtos com movimentacoes de estoque registradas (preservacao do historico de auditoria).

---

### 5. Movimentacoes (`/movimentacoes`)

#### `GET /movimentacoes`
Consulta avancada do historico de auditoria com filtros combinaveis e ordenacao da mais recente para a mais antiga.

- **Acesso:** Autenticado (`admin`, `gerente`, `estoquista`).
- **Parametros de Query (opcionais):**
  - `data_inicio`: data/hora inicial em formato ISO (ex: `2026-10-01T00:00:00Z`).
  - `data_fim`: data/hora final em formato ISO (ex: `2026-10-31T23:59:59Z`).
  - `tipo`: tipo de operacao (`ENTRADA` ou `SAIDA`).
  - `fornecedor_id`: UUID do fornecedor para auditoria cruzada por parceiro comercial.
- **Resposta de Sucesso (`200 OK`):**
```json
[
  {
    "id": "76eef5a2-386b-4e68-96bb-7d8481ff248a",
    "produto_id": "e9fbaf3b-a827-4a0b-85d7-386d63ff4be9",
    "tipo": "ENTRADA",
    "quantidade": 50,
    "valor_unitario": 35.00,
    "data": "2026-10-25T14:30:00Z"
  }
]
```

#### `GET /movimentacoes/produto/{produto_id}`
Extrato completo de movimentacoes de um unico produto.

- **Acesso:** Autenticado (`admin`, `gerente`, `estoquista`).
- **Resposta de Sucesso (`200 OK`):** Lista cronologica das entradas e saidas do produto indicado.

#### `POST /movimentacoes`
Registra uma entrada ou saida de mercadoria e atualiza o saldo de estoque atomicamente.

- **Acesso:** Autenticado (`admin`, `gerente`, `estoquista`).
- **Corpo da Requisicao (`application/json`):**
```json
{
  "produto_id": "e9fbaf3b-a827-4a0b-85d7-386d63ff4be9",
  "tipo": "SAIDA",
  "quantidade": 2,
  "valor_unitario": null
}
```
- **Regras Operacionais:**
  - Em movimentacoes de **SAIDA**, o `valor_unitario` assume automaticamente o preco de venda vigente do produto, e o estoque é deduzido. Caso a quantidade solicitada seja maior que o saldo atual, a operacao é rejeitada.
  - Em movimentacoes de **ENTRADA**, a quantidade é somada ao estoque. Se informado `valor_unitario`, o `preco_custo` cadastral do produto é atualizado para refletir o custo mais recente de aquisicao.
- **Resposta de Sucesso (`201 Created`):**
```json
{
  "id": "fa12c9b1-50e5-4f76-92c2-80ba497ea4f9",
  "produto_id": "e9fbaf3b-a827-4a0b-85d7-386d63ff4be9",
  "tipo": "SAIDA",
  "quantidade": 2,
  "valor_unitario": 89.90,
  "data": "2026-10-25T15:10:00Z"
}
```
- **Respostas de Erro:**
  - `400 Bad Request`: Quantidade solicitada de saida maior do que o saldo em estoque.
  - `404 Not Found`: Produto nao encontrado.
  - `422 Unprocessable Entity`: Quantidade menor ou igual a zero ou tipo de movimentacao invalido.

---

### 6. Dashboard Estrategico (`/dashboard`)

#### `GET /dashboard`
Endpoint analitico para tomada de decisao dos administradores e gerentes da loja.

- **Acesso:** `admin`, `gerente`.
- **Resposta de Sucesso (`200 OK`):**
```json
{
  "produto_mais_vendido": {
    "id": "e9fbaf3b-a827-4a0b-85d7-386d63ff4be9",
    "nome": "Fone de Ouvido Bluetooth Sem Fio",
    "quantidade_vendida": 142
  },
  "totais_30_dias": {
    "entradas": {
      "quantidade": 320,
      "valor_reais": 11200.00
    },
    "saidas": {
      "quantidade": 210,
      "valor_reais": 18879.00
    }
  },
  "grafico_diario": [
    {
      "data": "2026-10-20",
      "entradas_qtd": 50,
      "entradas_rs": 1750.00,
      "saidas_qtd": 15,
      "saidas_rs": 1348.50
    }
  ],
  "estoque_atual": [
    {
      "id": "e9fbaf3b-a827-4a0b-85d7-386d63ff4be9",
      "nome": "Fone de Ouvido Bluetooth Sem Fio",
      "qtd_estoque": 110
    }
  ],
  "produtos_estoque_critico": 4
}
```

---

## Consultas Avancadas e Inteligencia de Negocio

A API foi projetada para atender aos requisitos de analise estrategica solicitados no desafio:

1. **Filtro Temporal e de Fornecedores (`GET /movimentacoes`):**
   Permite correlacionar movimentacoes por periodo e identificar o fluxo de mercadorias atrelado a um fornecedor especifico. Utiliza juncao interna entre a tabela de produtos e a de movimentacoes para filtrar de forma eficiente no banco.
2. **Monitoramento de Ruptura de Estoque (`GET /produtos/alerta-estoque`):**
   Permite aos estoquistas e gerentes configurar gatilhos de reposicao, filtrando produtos com estoque igual ou abaixo do patamar critico desejado.
3. **Agrupamento Temporal e Consolidacao Financeira (`GET /dashboard`):**
   Utiliza funcoes de agregacao SQL (`SUM`, `GROUP BY`, `CAST(data AS Date)`) para fornecer visao historica dos ultimos 30 dias com volume de unidades e montante financeiro negociado por dia.

---

## Padroes de Commit e Codigo

### Convencao de Commits (Conventional Commits)
O projeto adota o padrao semantico de commits:
- `feat:` Inclusao de novas funcionalidades (ex: `feat: adicionar endpoint de dashboard analitico`).
- `fix:` Correcao de falhas ou bugs (ex: `fix: ajustar calculo de valor unitario na saida`).
- `docs:` Modificacoes na documentacao (ex: `docs: atualizar README com especificacoes completas`).
- `refactor:` Refatoracao de codigo sem alteracao de comportamento (ex: `refactor: isolar repositorios em queries dedicadas`).
- `chore:` Ajustes em configuracoes, build ou dependencias (ex: `chore: adicionar configuracao inicial do docker-compose`).

### Codigo Limpo e Tipagem Estrita
- **Nomenclatura PEP 8:** modulos, funcoes e variaveis em `snake_case`; classes em `PascalCase`.
- **Ausencia de `Any`:** Todas as funcoes, parametros e retornos possuem anotacoes explicitas de tipo.
