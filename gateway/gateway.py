import secrets

from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Разрешенные источники (только твой фронтенд-домен)
origins = [
    "https://gun.muduck.com",  # фронтенд
]

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Разрешенные источники (только твой фронтенд-домен)
origins = [
    "https://gun.muduck.com",  # фронтенд
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # какие домены могут ходить к API
    allow_credentials=True,
    allow_methods=["*"],            # какие методы (GET, POST и т.д.)
    allow_headers=["*"],            # какие заголовки
)
class SessionRequest(BaseModel):
    user_id: str

@app.post("/create_session")
async def create_session(req: SessionRequest):
    # ⚡ тут логика запуска воркера (пока заглушка)
    host = "gun-work-1.muduck.com"   # адрес машины/воркера
    port = 443                # порт, на котором он слушает
    token = secrets.token_hex(16)  # простой токен

    return {
        "host": host,
        "port": port,
        "token": token,
        "user_id": req.user_id
    }

# 🔹 сам WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            msg = await ws.receive_text()
            print(f"Got message: {msg}")
            await ws.send_text(f"Echo: {msg}")
    except Exception as e:
        print(f"WS closed: {e}")
    finally:
        await ws.close()