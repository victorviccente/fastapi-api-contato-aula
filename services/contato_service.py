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
