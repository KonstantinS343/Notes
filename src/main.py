from fastapi import FastAPI

import sys

sys.path = ['', '..'] + sys.path[1:]

from src.task.router import router as task_router

app = FastAPI(title='Notes')

app.include_router(task_router)
