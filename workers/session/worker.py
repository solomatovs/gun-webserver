# worker.py
import subprocess
from fastapi import FastAPI
from pydantic import BaseModel
import secrets
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["https://gun.muduck.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SessionRequest(BaseModel):
    user_id: str

@app.post("/start_session")
async def start_session(req: SessionRequest):
    token = secrets.token_hex(16)

    # запускаем user_ws_server.py
    proc = subprocess.Popen(
        ["python3", "user_ws_server.py", req.user_id],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # читаем первую строку stdout = порт, на котором поднялся WS сервер
    port_line = proc.stdout.readline().strip()
    port = int(port_line)

    # возвращаем gateway информацию фронту
    return {
        "host": "gate.muduck.com",
        "port": port,
        "token": token,
        "user_id": req.user_id
    }