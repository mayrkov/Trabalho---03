from pydantic import BaseModel, ConfigDict, Field


class ItemPedidoCreate(BaseModel):
    pedido_id: int = Field(..., gt=0, examples=[1])
    produto_id: int = Field(..., gt=0, examples=[1])
    quantidade: int = Field(..., gt=0, examples=[2])


class ItemPedidoUpdate(BaseModel):
    quantidade: int = Field(..., gt=0, examples=[3])


class ItemPedidoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    pedido_id: int
    produto_id: int
    quantidade: int
    subtotal: float