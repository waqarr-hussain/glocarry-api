from fastapi import FastAPI
from routers.products import router as products_router


app = FastAPI(
    title="Glocarry API",
    description="Grocery Ordering Platform API",
    version="1.0.0"
)


# Products router ko application mein include karna
app.include_router(products_router)


@app.get("/", status_code=200)
def home():
    return {
        "message": "Welcome to Glocarry API"
    }