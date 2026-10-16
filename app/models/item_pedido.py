from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    pedido_id: Mapped[int] = mapped_column(
        ForeignKey("pedidos.id"), nullable=False, index=True
    )
    produto_id: Mapped[int] = mapped_column(
        ForeignKey("produtos.id"), nullable=False, index=True
    )
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    subtotal: Mapped[float] = mapped_column(Float, nullable=False)

    pedido: Mapped["Pedido"] = relationship(  # noqa: F821
        "Pedido", back_populates="itens"
    )
    produto: Mapped["Produto"] = relationship(  # noqa: F821
        "Produto", back_populates="itens"
    )