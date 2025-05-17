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
