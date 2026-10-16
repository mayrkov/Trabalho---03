from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Pedido(Base):
    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("clientes.id"), nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="aberto")
    valor_total: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )

    cliente: Mapped["Cliente"] = relationship(  # noqa: F821
        "Cliente", back_populates="pedidos"
    )
    itens: Mapped[list["ItemPedido"]] = relationship(  # noqa: F821
        "ItemPedido", back_populates="pedido", cascade="all, delete-orphan"
    )
