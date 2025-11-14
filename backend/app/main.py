from fastapi import FastAPI
from .routes_products import router as product_router

app = FastAPI()

app.include_router(product_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
