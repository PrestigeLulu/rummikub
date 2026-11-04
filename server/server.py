import socketio
from fastapi import FastAPI

sio = socketio.AsyncServer(async_mode="asgi")
app = FastAPI()
board= [];

@sio.event
async def connect(sid, environ, auth):
    print("접속:", sid)

@sio.on("join")
async def join(sid, data):
    print("참가:", data)
    await sio.emit("welcome", {"message": "환영합니다!"}, to=sid)

@sio.on("play")
async def play(sid, data):
    board = data["board"]

@sio.event
async def disconnect(sid, reason):
    print("종료:", sid)

app = socketio.ASGIApp(sio, other_asgi_app=app)