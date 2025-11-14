from fastapi import FastAPI
from .routes_products import router as product_router
from .tasks import add_numbers

app = FastAPI()

app.include_router(product_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/run-task")
def run_task():
    task = add_numbers.delay(5, 7)
    return {"task_id": task.id}
