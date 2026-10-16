from pydantic import BaseModel, ConfigDict, Field


class ClienteCreate(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100, examples=["Ana Souza"])
    telefone: str = Field(..., min_length=8, max_length=20, examples=["(61) 99999-0000"])
    endereco: str = Field(
        ..., min_length=1, max_length=255, examples=["Rua das Flores, 123 - Centro"]
    )


class ClienteUpdate(BaseModel):
    nome: str | None = Field(None, min_length=1, max_length=100)
    telefone: str | None = Field(None, min_length=8, max_length=20)
    endereco: str | None = Field(None, min_length=1, max_length=255)


class ClienteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    telefone: str
    endereco: str
