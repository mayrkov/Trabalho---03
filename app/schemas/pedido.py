from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

StatusPedido = Literal["aberto", "em_preparo", "saiu_para_entrega", "entregue", "cancelado"]


class PedidoCreate(BaseModel):
    cliente_id: int = Field(..., gt=0, examples=[1])


class PedidoUpdate(BaseModel):
    status: StatusPedido = Field(..., examples=["em_preparo"])


class PedidoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cliente_id: int
    status: StatusPedido
    valor_total: float
    criado_em: datetime
