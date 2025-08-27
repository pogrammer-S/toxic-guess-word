# toxic-guess-word

## Скачивание модели
Модель: ruwikiruscorpora_upos_cbow_300_10_2021
Скачать на https://rusvectores.org/ru/models/
Поместить в backend/src/model

## Структура
```
toxic-guess-word/
  ├── docker-compose.yml   
  └── README.md
  backend/
    │
    ├── main.py                      
    ├── Dockerfile                    
    ├── requirements.txt
    ├── .env
    ├── src/
    │   ├──dependency_injection.py
    │   ├── application/
    │   │   ├── __init__.py        
    │   │   └── game_service.py         
    │   ├── config/
    │   │   └── config.py            
    │   ├── database/
    │   │   ├── __init__.py      
    │   │   ├── connection.py        
    │   │   └── init.sql             
    |   ├── domain/
    |   |   ├── __init__.py
    │   │   ├── game_engine.py
    |   |   ├── interfaces.py
    │   └── fastapi/
    │   |   ├── __init__.py
    │   |   ├── handler_fastapi.py
    |   ├── infrastructure/
    |   |   ├── __init__.py
    │   │   ├── game_repository.py
    |   |   ├── word_model.py
    |   ├── infrastructure/
    |   |   ├── __init__.py
    │   │   ├── connect.py
    |   |   ├── meta.json
    |   |   ├── model.bin  
  bot/
    │
    ├── main.py                      
    ├── Dockerfile                    
    ├── requirements.txt
    ├── .env
    ├── src/
    │   ├── backend/
    │   │   ├── __init__.py        
    │   │   └── back_service.py      
    │   ├── config/
    │   │   └── config.py            
    │   ├── database/
    │   │   ├── __init__.py      
    │   │   ├── connection.py
    |   │   ├── db_services.py
    │   │   └── init.sql             
    |   ├── bot/
    |   |   ├── __init__.py
    │   │   ├── bot.py
    |   |   ├── command.py
    |   |   ├── handler.py

```
## Быстрый старт

### 1. Клонируйте репозиторий

```bash
git clone <repo-url>
cd tg-bot-listener
```

### 2. Создайте файл `.env` в backend и bot по образцам .env.example

```env
# bot
BOT_TOKEN=BOT_TOKEN
API_URL=http://game:80/api/v1/game/

DB_HOST=DB_HOST
DB_NAME=DB_NAME
DB_USER=DB_USER
DB_PASSWORD=DB_PASSWORD
DB_PORT=DB_PORT

# backend
DB_HOST=DB_HOST
DB_NAME=DB_NAME
DB_USER=DB_USER
DB_PASSWORD=DB_PASSWORD
DB_PORT=DB_PORT
```

```bash
docker-compose up -d --build
```
