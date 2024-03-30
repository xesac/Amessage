import secrets
from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, Form, Request
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr

from db_redis.redis import get_redis
from tasks.task import send_message_confirmation_email

templates = Jinja2Templates(directory='templates')


router = APIRouter(prefix='/message', tags=['Анонимные сообщения'])


@router.get('')
async def main_page(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@router.get('/get')
async def get_message(request: Request):
    return templates.TemplateResponse('get_message.html', {'request': request})


@router.get('/get/{key}')
async def get_secret_message(
    key: str, request: Request, redis=Depends(get_redis)
):
    try:
        message = await redis.get(key)
        ttl = await redis.ttl(key)
        res = None
        if message:
            res = message.decode('utf-8')
        else:
            res = 'Неверный ключ или сообщение уже удалено'
        return templates.TemplateResponse(
            'show_message.html', {'request': request, 'message': res, 'time': ttl}
        )
    except:
        return templates.TemplateResponse('500.html', {'request': request})


@router.get('/create')
async def create_message_page(request: Request):
    return templates.TemplateResponse(
        'create_message.html', {'request': request}
    )


@router.get('/after_create')
async def after_create(request: Request):
    return templates.TemplateResponse(
        'after_create.html', {'request': request}
    )


@router.post('/create')
async def create_message(
    message: Annotated[str, Form()],
    email: Annotated[EmailStr, Form()],
    request: Request,
    redis=Depends(get_redis),
):
    if len(message) > 1000:
        return templates.TemplateResponse('len.html', {'request': request})
    else:
        try:
            secret_key = secrets.token_hex(30)
            await redis.set(
                secret_key, message, ex=timedelta(minutes=30)
            )
            send_message_confirmation_email(secret_key, email)
            return templates.TemplateResponse(
                'after_create.html', {'request': request, 'secret_key': secret_key}
            )
        except:
            return templates.TemplateResponse('500.html', {'request': request})

