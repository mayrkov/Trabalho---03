# Pizzaria API

API de delivery de pizzas desenvolvida para o Trabalho Prático 03 da disciplina de
Arquitetura de Software (Bloco IV – 2026.2).

**Stack:** FastAPI · SQLAlchemy (ORM) · Alembic (migrações) · SQLite · Poetry

## Descrição

A API gerencia **clientes**, o **cardápio de produtos** (pizzas e bebidas) e os
**pedidos** — cada pedido pertence a um cliente e é composto por itens escolhidos do
cardápio.

### Entidades e relacionamentos

```
Cliente   1 ──── N Pedido
Pedido    1 ──── N ItemPedido
Produto   1 ──── N ItemPedido
```

| Entidade | Atributos principais |
|----------|----------------------|
| `Cliente` | id, nome, telefone, endereco |
| `Produto` | id, nome, descricao, preco |
| `Pedido` | id, cliente_id, status, valor_total, criado_em |
| `ItemPedido` | id, pedido_id, produto_id, quantidade, subtotal |

## Estrutura de pastas

```
trabalho-pratico-03/
├── app/
│   ├── core/       config.py, database.py
│   ├── models/     produto.py, cliente.py, pedido.py, item_pedido.py
│   ├── schemas/    produto.py, cliente.py, pedido.py, item_pedido.py
│   ├── routers/    produto.py, cliente.py, pedido.py, item_pedido.py
│   └── main.py
├── alembic/
├── alembic.ini
├── assets/         diagrama.drawio, diagrama.png
└── README.md
```

## Configuração do ambiente (para todos os integrantes)

> Vale para **Linux, macOS e Windows**. O Poetry cria o ambiente virtual sozinho,
> então quase não há diferença entre os sistemas.

### 1. Pré-requisitos

- **Python 3.12+** — https://www.python.org/downloads/
  (no Windows, marque **"Add Python to PATH"** durante a instalação)
- **Git** — https://git-scm.com/downloads
- **Poetry** — instalador oficial:

  **Linux / macOS:**
  ```bash
  curl -sSL https://install.python-poetry.org | python3 -
  ```
  **Windows (PowerShell):**
  ```powershell
  (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
  ```

  Feche e reabra o terminal depois de instalar. Confira com:
  ```bash
  poetry --version
  ```

### 2. Clonar o repositório

```bash
git clone <URL-DO-REPOSITORIO>
cd trabalho-pratico-03
```

### 3. Instalar as dependências

```bash
poetry install
```

Isso cria o ambiente virtual e instala FastAPI, SQLAlchemy e Alembic exatamente nas
versões do `poetry.lock`.

### 4. Criar o banco (migrações)

```bash
poetry run alembic upgrade head
```

### 5. Rodar a aplicação

```bash
poetry run uvicorn app.main:app --reload
```

A documentação interativa (Swagger) fica disponível em http://127.0.0.1:8000/docs.

### Importante: sempre use `poetry run`

Todos os comandos (`alembic`, `uvicorn`, `python`) rodam **dentro** do ambiente virtual.
A forma mais simples e **igual nos 3 sistemas** é prefixar com `poetry run` — assim você
**não precisa ativar nada manualmente**.

Se ainda quiser ativar o ambiente manualmente, primeiro descubra a pasta do venv:

```bash
poetry env info --path
```

E então:

- **Linux / macOS:** `source <caminho>/bin/activate`
- **Windows (cmd):** `<caminho>\Scripts\activate`
- **Windows (PowerShell):** `<caminho>\Scripts\Activate.ps1`

### Rode os comandos a partir da raiz do projeto

Execute tudo **de dentro da pasta do projeto** (onde está o `alembic.ini`), senão o
Alembic pode não encontrar o pacote `app`.

### Fluxo de trabalho de cada integrante

```bash
git pull
git checkout -b feature/<sua-entidade>
# ... cria app/models/<entidade>.py, app/schemas/<entidade>.py e app/routers/<entidade>.py ...
# ... importa o model em app/models/__init__.py ...
git add .
git commit -m "feat(<entidade>): model, schemas e router"
git push -u origin feature/<sua-entidade>
# depois: abrir um Pull Request no GitHub
```

### Erros comuns

- **"comando não encontrado"** (`alembic`, `uvicorn`, `poetry`) → use `poetry run ...`
  e/ou feche e reabra o terminal.
- **"No module named 'app'"** → você está fora da raiz do projeto; rode de dentro dela.
- **PowerShell bloqueando o `activate`** → use `poetry run` (evita o problema) ou rode
  `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`.

## Configurar o interpretador da IDE

Se a sua IDE (Antigravity, VS Code, Cursor, PyCharm…) mostrar **erros em imports** como
`from fastapi import FastAPI` ou `from alembic import context` — mesmo depois de rodar
`poetry install` — **quase sempre é porque a IDE está apontando para o Python errado**:
o ambiente **global da máquina** (ou outro qualquer), que **não tem** as dependências do
projeto instaladas.

O código está certo; quem está "olhando" para o lugar errado é a IDE. Para corrigir,
aponte a IDE para o **ambiente virtual do projeto**.

### Passo a passo (exemplo: Antigravity do Google / VS Code)

1. **Descubra o caminho do interpretador.** No terminal, **de dentro da pasta do
   projeto**, rode:
   ```bash
   poetry env info --executable
   ```
   Ele imprime o caminho completo do Python, por exemplo:
   - **Linux/macOS:** `/home/usuario/.cache/pypoetry/virtualenvs/trabalho-pratico-03-XXXX-py3.12/bin/python`
   - **Windows:** `C:\Users\usuario\AppData\Local\pypoetry\Cache\virtualenvs\trabalho-pratico-03-XXXX-py3.12\Scripts\python.exe`

2. **Copie esse caminho inteiro.**

3. Abra a **paleta de comandos**: `Ctrl + Shift + P` (no macOS, `Cmd + Shift + P`).

4. Digite e selecione **Python: Select Interpreter**
   (em pt-br: *Python: Selecionar Interpretador*).

5. Escolha **Enter interpreter path...** (*Inserir caminho do interpretador…*)
   e depois **Find... / Encontrar**.

6. **Cole o caminho** copiado no passo 2 e confirme.

7. **Reabra o arquivo** (ou a janela da IDE). Os avisos de import somem e o autocomplete
   passa a reconhecer FastAPI, SQLAlchemy e Alembic.

### Em outras IDEs

O caminho do interpretador é sempre o mesmo (passo 1); muda só onde fica a opção:

- **VS Code / Cursor / Antigravity (do Google):** `Ctrl + Shift + P` →
  *Python: Select Interpreter*.
- **PyCharm:** `Settings` → `Project` → `Python Interpreter` → `Add Interpreter` →
  `Existing` → aponte para o executável do passo 1.

### Observações

- Isso **não afeta** o funcionamento do projeto — é só para o editor parar de marcar
  imports como erro e melhorar o autocomplete.
- Se você roda tudo pelo terminal com `poetry run ...`, o projeto funcionará mesmo que
  a IDE continue com o interpretador errado.

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/health` | Verificação de saúde da API |
| GET | `/produtos` | Lista produtos |
| GET | `/produtos/{id}` | Busca produto |
| POST | `/produtos` | Cria produto (201) |
| PUT | `/produtos/{id}` | Atualiza produto |
| DELETE | `/produtos/{id}` | Remove produto (204) |
| GET | `/clientes` | Lista clientes |
| GET | `/clientes/{id}` | Busca cliente |
| POST | `/clientes` | Cria cliente (201) |
| PUT | `/clientes/{id}` | Atualiza cliente |
| DELETE | `/clientes/{id}` | Remove cliente (204) |
| GET | `/pedidos` | Lista pedidos |
| GET | `/pedidos/{id}` | Busca pedido |
| POST | `/pedidos` | Cria pedido (valida cliente — 201) |
| PATCH | `/pedidos/{id}/status` | Atualiza status |
| DELETE | `/pedidos/{id}` | Remove pedido (204) |
| GET | `/itens` | Lista itens |
| GET | `/itens/{id}` | Busca item |
| POST | `/itens` | Cria item (valida pedido e produto — 201) |
| PUT | `/itens/{id}` | Atualiza item |
| DELETE | `/itens/{id}` | Remove item (204) |

## Equipe

| Nome | Responsabilidade |
|------|------------------|
| Mayk | Infraestrutura, integração e migrações |
| Mairon | Diagramas + `Produto` |
| Miguel | `Cliente` |
| Daniel | `Pedido` |
| Wendhel | `ItemPedido` |
