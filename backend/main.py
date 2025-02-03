from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
import socketio
from pydantic import BaseModel
from typing import List

# FastAPI app
app = FastAPI()

# Serve static files (frontend)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# SocketIO server
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
socket_app = socketio.ASGIApp(sio, app)

# Data models
class Sprite(BaseModel):
    id: str
    x: float
    y: float
    image: str  # URL or path to the sprite image

class UIState(BaseModel):
    zoom: float
    pan_x: float
    pan_y: float

# In-memory storage for sprites and UI state
sprites: List[Sprite] = []
ui_state = UIState(zoom=1.0, pan_x=0.0, pan_y=0.0)

# SocketIO events
@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    await sio.emit("update_sprites", sprites)
    await sio.emit("update_ui_state", ui_state.dict())

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.event
async def update_sprite(sid, data):
    sprite = Sprite(**data)
    for i, s in enumerate(sprites):
        if s.id == sprite.id:
            sprites[i] = sprite
            break
    else:
        sprites.append(sprite)
    await sio.emit("update_sprites", sprites)

@sio.event
async def update_ui_state(sid, data):
    global ui_state
    ui_state = UIState(**data)
    await sio.emit("update_ui_state", ui_state.dict())

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(socket_app, host="0.0.0.0", port=8000)
