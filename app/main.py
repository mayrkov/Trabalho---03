from fastapi import FastAPI

app = FastAPI(
    title="Pizzaria API",
    description="API de delivery de pizzas: clientes, cardapio e pedidos.",
    version="0.1.0",
)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
