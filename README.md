# API de Gerenciamento de Contatos com FastAPI

Este repositório contém uma API RESTful para gerenciamento de contatos desenvolvida como material didático, implementada com o framework FastAPI utilizando uma arquitetura em camadas.

## 📋 Características

- Arquitetura em camadas (Models, Routes, Services)
- Operações CRUD completas
- Validação de dados com Pydantic
- Documentação automática com Swagger/OpenAPI

## 🏗️ Estrutura do Projeto

```
contatos_crud/
├── main.py                  # Ponto de entrada da aplicação
├── models/                  # Modelos de dados
│   └── contato.py
├── routes/                  # Definições de rotas
│   └── contato_routes.py
└── services/                # Lógica de negócios
    └── contato_service.py
```

## 🚀 Instalação e Execução

### Pré-requisitos

- Python 3.8+
- FastAPI
- Uvicorn (servidor ASGI)
- Pydantic (validação de dados)
- email-validator (validação de e-mail)

### Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/fastapi-api-contato-aula.git
   cd fastapi-api-contato-aula
   ```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   # No Windows:
   venv\Scripts\activate
   # No Linux/macOS:
   source venv/bin/activate
   ```

3. Instale as dependências necessárias:
   ```bash
   pip install fastapi uvicorn pydantic email-validator
   ```

4. Execute a aplicação:
   ```bash
   uvicorn main:app --reload
   ```

5. Acesse a API em [http://localhost:8000](http://localhost:8000)
   - Interface Swagger para testar a API: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Documentação alternativa: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 📝 Componentes Principais

### 1. Modelo de Dados (`models/contato.py`)

```python
from pydantic import BaseModel, EmailStr
from typing import Optional

class Contato(BaseModel):
    id: Optional[int] = None
    nome: str
    telefone: str
    email: EmailStr
```

### 2. Serviço de Contatos (`services/contato_service.py`)

```python
from typing import List, Optional
from models.contato import Contato

contatos: List[Contato] = []
proximo_id: int = 1

def listar() -> List[Contato]:
    return contatos

def buscar_por_nome(nome: str) -> List[Contato]:
    return [c for c in contatos if nome.lower() in c.nome.lower()]

def obter_por_id(id: int) -> Optional[Contato]:
    return next((c for c in contatos if c.id == id), None)

def criar(contato: Contato) -> Contato:
    global proximo_id
    novo_contato = contato.copy(update={"id": proximo_id})
    contatos.append(novo_contato)
    proximo_id += 1
    return novo_contato

def atualizar(id: int, contato_atualizado: Contato) -> Optional[Contato]:
    for index, c in enumerate(contatos):
        if c.id == id:
            contatos[index] = contato_atualizado.copy(update={"id": id})
            return contatos[index]
    return None

def remover(id: int) -> bool:
    global contatos
    for c in contatos:
        if c.id == id:
            contatos = [c for c in contatos if c.id != id]
            return True
    return False
```

### 3. Rotas API (`routes/contato_routes.py`)

```python
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from models.contato import Contato
import services.contato_service as service

router = APIRouter()

@router.get("", response_model=List[Contato])
def listar_contatos():
    return service.listar()

@router.get("/buscar", response_model=List[Contato])
def buscar_contato(nome: Optional[str] = Query(None, min_length=1)):
    if not nome:
        raise HTTPException(status_code=400, detail="Parâmetro 'nome' obrigatório.")
    return service.buscar_por_nome(nome)

@router.get("/{id}", response_model=Contato)
def obter_contato(id: int):
    contato = service.obter_por_id(id)
    if not contato:
        raise HTTPException(status_code=404, detail="Contato não encontrado!")
    return contato

@router.post("", response_model=Contato, status_code=201)
def criar_contato(contato: Contato):
    return service.criar(contato)

@router.put("/{id}", response_model=Contato)
def atualizar_contato(id: int, contato_atualizado: Contato):
    contato = service.atualizar(id, contato_atualizado)
    if not contato:
        raise HTTPException(status_code=404, detail="Contato não encontrado!")
    return contato

@router.delete("/{id}", response_model=dict)
def apagar_contato(id: int):
    sucesso = service.remover(id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Contato não encontrado!")
    return {"mensagem": "Contato removido"}
```

### 4. Aplicação Principal (`main.py`)

```python
from fastapi import FastAPI
from routes.contato_routes import router as contato_router

app = FastAPI()
app.include_router(contato_router, prefix="/contatos", tags=["Contatos"])
```

## 🔄 Endpoints da API

| Método | Endpoint            | Descrição                          |
|--------|---------------------|-----------------------------------|
| GET    | /contatos           | Lista todos os contatos           |
| GET    | /contatos/buscar?nome={nome} | Busca contatos pelo nome |
| GET    | /contatos/{id}      | Obtém um contato pelo ID          |
| POST   | /contatos           | Cria um novo contato              |
| PUT    | /contatos/{id}      | Atualiza um contato existente     |
| DELETE | /contatos/{id}      | Remove um contato                 |

## 🧪 Testando a API

A maneira mais fácil de testar a API é utilizar a interface Swagger UI disponível em [http://localhost:8000/docs](http://localhost:8000/docs) após iniciar a aplicação. A interface permite:

- Visualizar todos os endpoints disponíveis
- Testar cada operação diretamente no navegador
- Ver os modelos de dados e esquemas
- Executar requisições e visualizar respostas em tempo real

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

## 🔍 Próximos Passos

- Implementar persistência de dados com um banco de dados
- Adicionar autenticação e autorização
- Implementar testes automatizados
- Configurar um ambiente de produção

## 📜 Licença

Este projeto é disponibilizado sob a licença MIT.
