from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.cliente import Cliente
from app.models.pedido import Pedido
from app.schemas.pedido import PedidoCreate, PedidoResponse, PedidoUpdate

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


def buscar_pedido_ou_404(pedido_id: int, db: Session) -> Pedido:
    pedido = db.get(Pedido, pedido_id)
    if pedido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pedido {pedido_id} não encontrado",
        )
    return pedido


@router.get("", response_model=list[PedidoResponse])
def listar_pedidos(db: Session = Depends(get_db)):
    return db.query(Pedido).order_by(Pedido.id).all()


@router.get("/{pedido_id}", response_model=PedidoResponse)
def buscar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    return buscar_pedido_ou_404(pedido_id, db)


@router.post("", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
def criar_pedido(dados: PedidoCreate, db: Session = Depends(get_db)):
    # Requisito 8: valida a integridade da FK antes de inserir
    if db.get(Cliente, dados.cliente_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente {dados.cliente_id} não encontrado",
        )
    pedido = Pedido(cliente_id=dados.cliente_id)
    db.add(pedido)
    db.commit()
    db.refresh(pedido)
    return pedido


@router.patch("/{pedido_id}/status", response_model=PedidoResponse)
def atualizar_status_pedido(
    pedido_id: int, dados: PedidoUpdate, db: Session = Depends(get_db)
):
    pedido = buscar_pedido_ou_404(pedido_id, db)
    pedido.status = dados.status
    db.commit()
    db.refresh(pedido)
    return pedido


@router.delete("/{pedido_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = buscar_pedido_ou_404(pedido_id, db)
    db.delete(pedido)  # cascade remove os itens do pedido
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
