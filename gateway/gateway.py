# gateway.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import secrets

app = FastAPI()
origins = ["https://gun.muduck.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Данные запроса от фронтенда ---
class CreateSessionRequest(BaseModel):
    user_id: str

# --- Конфиг воркеров ---
WORKERS = [
    {"host": "gun-work-1.muduck.com", "port": 443}  # Можно добавить несколько воркеров
]

@app.post("/create_session")
async def create_session(req: CreateSessionRequest):
    # выбираем воркера (например, первый в списке)
    worker = WORKERS[0]
    worker_url = f"https://{worker['host']}:{worker['port']}/start_session"

    # генерируем токен для WS
    token = secrets.token_hex(16)

    # отправляем запрос воркеру
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(worker_url, json={"user_id": req.user_id})
            resp.raise_for_status()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"Worker error: {e}")

    data = resp.json()
    # добавляем токен
    data["token"] = token

    # возвращаем фронтенду host, port, token
    return data