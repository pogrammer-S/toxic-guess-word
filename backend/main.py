import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse

from src.fastapi.handler_fastapi import router

app = FastAPI()

# Включаем роутер API
app.include_router(router)