# AGENTS.MD - Diretrizes do Projeto

## Contexto do Projeto
API RESTful para gerenciamento de estoque da "愚公移山 Variedades". O núcleo do sistema gerencia o ciclo de vida do estoque (CRUD de produtos, categorias e fornecedores), registro de movimentações (entradas/saídas) e autenticação de usuários (login/registro).

## Stack e Arquitetura
- **Back-end:** FastAPI
- **ORMs e Banco:** SQLAlchemy + PostgreSQL
- **Validação:** Pydantic
- **Infraestrutura:** Docker + docker-compose + Makefile

### Estrutura de Pastas (Clean Architecture)
A estrutura base do projeto é listada abaixo. 

Este arquivo `AGENTS.md` é a documentação do projeto. Sempre que você (IA) sugerir a criação de uma nova pasta, domínio (ex: `sales/`) ou arquivo estrutural, você **DEVE** editar este arquivo `AGENTS.md` adicionando a nova rota/pasta na árvore de diretórios abaixo. Nunca deixe essa árvore desatualizada em relação ao código real. 

NÃO reproduza a árvore inteira nas suas respostas do chat para poupar tokens; apenas edite o arquivo silenciosamente quando houver mudanças.

app/
├── api/             # Endpoints (routes.py) e dependências de rotas
├── core/            # Configurações globais (security, config.py)
├── enums/           # Classes Enum do Python
├── models/          # Modelos do SQLAlchemy (Tabelas do Banco)
├── repositories/    # Lógica de acesso a dados (Queries isoladas)
├── schemas/         # Modelos Pydantic (Validação de I/O)
├── services/        # Regras de negócio
├── utils/           # Funções auxiliares genéricas
└── main.py          # Ponto de entrada do Uvicorn

## Padrões de Código e Convenções

### Nomenclatura Estrita (PEP 8)
- **Pastas e Arquivos:** `snake_case` OBRIGATÓRIO (ex: `auth_service.py`, `user_repository.py`, `product_schemas.py`). NUNCA use camelCase em arquivos Python.
- **Variáveis e Funções:** `snake_case` com nomes descritivos.
- **Classes (Models, Schemas, Services):** `PascalCase` (ex: `ProductCreate`, `AuthService`).

### Comentários e Documentação
- NÃO escreva meta-comentários, placeholders ou dicas de ações futuras (ex: "Altere isso depois", "Coloque a rota aqui").
- NÃO se dirija ao usuário em primeira ou segunda pessoa ("Aqui você faz...").
- DEVE utilizar apenas comentários puramente descritivos e técnicos, explicando o **porquê** de uma lógica complexa existir, e não o que o código faz (o código limpo já diz o que faz).
- Pendências devem ser marcadas no formato `TODO: <ação clara e breve>`.

## Rotas, HTTP e Exceções

### Padrão RESTful
As rotas devem seguir estritamente o padrão REST. O método HTTP define a ação. NUNCA utilize verbos nas URLs.
- **Criar:** `POST /produtos` (Proibido: `/produtos/criar`)
- **Listar todos:** `GET /fornecedores` (Proibido: `/fornecedores/listar`)
- **Buscar um:** `GET /produtos/{id}` (Proibido: `/produto/buscar/{id}`)
- **Atualizar:** `PUT` ou `PATCH /fornecedores/{id}`
- **Remover:** `DELETE /produtos/{id}`

### Padrões de Respostas e Exceções
- **Camada de Serviço vs Rotas:** A regra de negócio DEVE viver na pasta `services/`. As rotas (`api/`) servem apenas para receber a requisição, chamar o service correspondente e retornar a resposta.
- **Tratamento de Erros:** O Service deve lançar exceções claras. A Rota deve capturá-las e retornar o erro HTTP correto (ex: `404 Not Found`, `400 Bad Request`, `409 Conflict`).
- **Segurança no Retorno:** É PROIBIDO expor `str(e)` ou detalhes internos do banco de dados no `detail` do `HTTPException`. Retorne mensagens formatadas e amigáveis ao usuário.

### RBAC (Role-Based Access Control)
- Proteja rotas sensíveis verificando os privilégios do usuário logado (ex: `admin`, `gerente`, `estoquista`).
- Rotas de auditoria e exclusão (`DELETE`) devem ser restritas a perfis de alto nível (admin).

## Segurança e Restrições Absolutas

### Gestão de Segredos
- É ESTRITAMENTE PROIBIDO fazer hardcode de senhas, tokens, URIs de banco ou chaves secretas no código (ex: `db_url = "postgresql://..."`).
- Todas as variáveis sensíveis DEVEM ser consumidas do ambiente. Utilize o pacote `pydantic-settings` para gerenciar essas variáveis na pasta `core/`.

### Práticas Bloqueadas (NÃO FAZER)
1. Criar arquivos fora da estrutura definida na Clean Architecture.
2. Usar o tipo `Any` do módulo `typing` em qualquer lugar (A tipagem deve ser estrita).
3. Utilizar emojis em commits, respostas, comentários ou docstrings.
4. Misturar regras de negócio dentro dos arquivos do SQLAlchemy (models).