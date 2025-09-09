# user_ws_server.py
import sys
import asyncio
from fastapi import FastAPI, WebSocket
import uvicorn
import socket

user_id = sys.argv[1]

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    count = 0
    try:
        while True:
            count += 1
            await ws.send_text(f"[{user_id}] Tick {count}")
            await asyncio.sleep(1)
    except:
        pass

if __name__ == "__main__":
    # выбираем свободный порт
    sock = socket.socket()
    sock.bind(("0.0.0.0", 0))  # порт 0 = ОС выбирает свободный
    host, port = sock.getsockname()
    sock.close()

    # сообщаем воркеру через stdout
    print(port, flush=True)

    # запускаем uvicorn на выбранном порту
    uvicorn.run(app, host="0.0.0.0", port=port)