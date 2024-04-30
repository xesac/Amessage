from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.staticfiles import StaticFiles

from db_redis.redis import get_redis
from routers.message_router import router as message_router
from routers.message_router import templates
import sentry_sdk
from config.config import settings


sentry_sdk.init(
    dsn=settings.DSN,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


@asynccontextmanager
async def lifespan(app: FastAPI, redis=Depends(get_redis)):
    FastAPICache.init(RedisBackend(redis), prefix='cache')
    print('Запущено')
    yield
    print('Завершено')


app = FastAPI(
    title='AMessage',
    lifespan=lifespan,
    description='Создание и чтение анонимных сообщений',
)

app.include_router(message_router)
app.mount("/static", StaticFiles(directory="static"), "static")

@app.get('/')
async def redirect():
    return RedirectResponse('/message')

@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse('404.html', {'request': request})


origins = ['http://localhost:8000']


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=['GET', 'POST'],
    allow_headers=[
        'Content-Type',
        'Access-Control-Allow-Headers',
        'Access-Control-Allow-Origin',
    ],
)
