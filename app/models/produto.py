from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Produto(Base):
    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    descricao: Mapped[str | None] = mapped_column(String(255), nullable=True)
    preco: Mapped[float] = mapped_column(Float, nullable=False)

    itens: Mapped[list["ItemPedido"]] = relationship(  # noqa: F821
        "ItemPedido", back_populates="produto"
    )
