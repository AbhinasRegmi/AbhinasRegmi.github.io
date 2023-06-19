from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from portfolio.app.api import router
from portfolio.app.api.middlewares.responsetime import ResponseTime
from portfolio.app.core.config import settings


@asynccontextmanager
async def lifespan():
    yield


app = FastAPI(
        title=settings.PROJECT_NAME,
        redoc_url='',
        docs_url='/'
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_CORS_ORIGIN,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.add_middleware(ResponseTime)


@app.get("/health", tags=['Health'])
def test_alive():
    return {
        "message": "alive"
    }


app.include_router(router=router.router)



# gunicorn src.portfolio.app.app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80