from fastapi import FastAPI

from app.routers import cliente, item_pedido, pedido, produto

app = FastAPI(
    title="Pizzaria API",
    description="API de delivery de pizzas: clientes, cardapio e pedidos.",
    version="0.1.0",
)

app.include_router(produto.router)
app.include_router(cliente.router)
app.include_router(pedido.router)
app.include_router(item_pedido.router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
