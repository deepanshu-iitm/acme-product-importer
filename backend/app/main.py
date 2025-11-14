from fastapi import FastAPI
from .routes_products import router as product_router
from .routes_upload import router as upload_router
from .tasks import add_numbers
from .routes_task import router as task_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(product_router)
app.include_router(upload_router)
app.include_router(task_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/run-task")
def run_task():
    task = add_numbers.delay(5, 7)
    return {"task_id": task.id}
