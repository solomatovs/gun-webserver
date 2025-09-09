import asyncio
import subprocess
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import secrets

# --- CORS ---
app = FastAPI()
origins = ["https://gun.muduck.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- POST /create_session ---
from pydantic import BaseModel

class SessionRequest(BaseModel):
    user_id: str

@app.post("/create_session")
async def create_session(req: SessionRequest):
    # Заглушка: токен для аутентификации WS
    token = secrets.token_hex(16)

    # Можно здесь запускать subprocess на произвольном порту или хранить инфо в Redis
    return {
        "host": "gate.muduck.com",  # адрес воркера
        "port": 9001,               # порт воркера (uvicorn)
        "token": token,
        "user_id": req.user_id
    }

# --- WebSocket endpoint ---
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        # Получаем user_id из query параметра
        user_id = ws.query_params.get("user_id", "anonymous")

        # Запускаем subprocess для конкретного user_id
        proc = subprocess.Popen(
            ["python3", "user_process.py", user_id],
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            text=True
        )

        loop = asyncio.get_event_loop()

        async def send_stdout():
            while True:
                line = await loop.run_in_executor(None, proc.stdout.readline)
                if not line:
                    break
                await ws.send_text(line.strip())

        async def receive_ws():
            try:
                while True:
                    data = await ws.receive_text()
                    if proc.stdin:
                        proc.stdin.write(data + "\n")
                        proc.stdin.flush()
            except WebSocketDisconnect:
                pass

        # Параллельно читаем stdout и слушаем websocket
        await asyncio.gather(send_stdout(), receive_ws())

    finally:
        proc.kill()
        await ws.close()
