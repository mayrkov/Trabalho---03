from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.item_pedido import ItemPedido
from app.models.pedido import Pedido
from app.models.produto import Produto
from app.schemas.item_pedido import (
    ItemPedidoCreate,
    ItemPedidoResponse,
    ItemPedidoUpdate,
)

router = APIRouter(prefix="/itens", tags=["Itens do Pedido"])


def buscar_item_ou_404(item_id: int, db: Session) -> ItemPedido:
    item = db.get(ItemPedido, item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} não encontrado",
        )
    return item


def recalcular_total(pedido: Pedido) -> None:
    pedido.valor_total = round(sum(item.subtotal for item in pedido.itens), 2)


@router.get("", response_model=list[ItemPedidoResponse])
def listar_itens(db: Session = Depends(get_db)):
    return db.query(ItemPedido).order_by(ItemPedido.id).all()


@router.get("/{item_id}", response_model=ItemPedidoResponse)
def buscar_item(item_id: int, db: Session = Depends(get_db)):
    return buscar_item_ou_404(item_id, db)


@router.post("", response_model=ItemPedidoResponse, status_code=status.HTTP_201_CREATED)
def criar_item(dados: ItemPedidoCreate, db: Session = Depends(get_db)):
    # Requisito 8: valida as duas FKs antes de inserir
    pedido = db.get(Pedido, dados.pedido_id)
    if pedido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pedido {dados.pedido_id} não encontrado",
        )
    produto = db.get(Produto, dados.produto_id)
    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produto {dados.produto_id} não encontrado",
        )

    item = ItemPedido(
        produto=produto,
        quantidade=dados.quantidade,
        subtotal=round(produto.preco * dados.quantidade, 2),
    )
    pedido.itens.append(item)
    recalcular_total(pedido)
    db.commit()
    db.refresh(item)
    return item


@router.put("/{item_id}", response_model=ItemPedidoResponse)
def atualizar_item(item_id: int, dados: ItemPedidoUpdate, db: Session = Depends(get_db)):
    item = buscar_item_ou_404(item_id, db)
    item.quantidade = dados.quantidade
    item.subtotal = round(item.produto.preco * dados.quantidade, 2)
    recalcular_total(item.pedido)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_item(item_id: int, db: Session = Depends(get_db)):
    item = buscar_item_ou_404(item_id, db)
    pedido = item.pedido
    pedido.itens.remove(item)  # delete-orphan apaga o item
    recalcular_total(pedido)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)