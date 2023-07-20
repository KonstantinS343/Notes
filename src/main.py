from fastapi import FastAPI

from src.task.router import router as task_router


app = FastAPI(title='Notes')

app.include_router(task_router)
