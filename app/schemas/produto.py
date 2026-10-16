from pydantic import BaseModel, ConfigDict, Field


class ProdutoCreate(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100, examples=["Pizza Calabresa"])
    descricao: str | None = Field(
        None, max_length=255, examples=["Molho, mussarela, calabresa e cebola"]
    )
    preco: float = Field(..., gt=0, examples=[49.90])


class ProdutoUpdate(BaseModel):
    nome: str | None = Field(None, min_length=1, max_length=100)
    descricao: str | None = Field(None, max_length=255)
    preco: float | None = Field(None, gt=0)


class ProdutoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    descricao: str | None
    preco: float
