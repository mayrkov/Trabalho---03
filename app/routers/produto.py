from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.produto import Produto
from app.schemas.produto import ProdutoCreate, ProdutoResponse, ProdutoUpdate

router = APIRouter(prefix="/produtos", tags=["Produtos"])


def buscar_produto_ou_404(produto_id: int, db: Session) -> Produto:
    produto = db.get(Produto, produto_id)
    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produto {produto_id} não encontrado",
        )
    return produto


@router.get("", response_model=list[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(Produto).order_by(Produto.id).all()


@router.get("/{produto_id}", response_model=ProdutoResponse)
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    return buscar_produto_ou_404(produto_id, db)


@router.post("", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def criar_produto(dados: ProdutoCreate, db: Session = Depends(get_db)):
    produto = Produto(**dados.model_dump())
    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto


@router.put("/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(
    produto_id: int, dados: ProdutoUpdate, db: Session = Depends(get_db)
):
    produto = buscar_produto_ou_404(produto_id, db)
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(produto, campo, valor)
    db.commit()
    db.refresh(produto)
    return produto


@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = buscar_produto_ou_404(produto_id, db)
    if produto.itens:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Produto está em itens de pedido e não pode ser removido",
        )
    db.delete(produto)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
