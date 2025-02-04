import socketio

# SocketIO server
sio = socketio.Server(cors_allowed_origins='http://localhost:3000', logger=True, engineio_logger=True)

# SocketIO events
@sio.event
def connect(sid, environ):
    print(f"Client connected: {sid}")
    # sio.emit("update_sprites", sprites)
    # sio.emit("update_ui_state", ui_state.dict())

@sio.event
def disconnect(sid):
    print(f"Client disconnected: {sid}")

# @sio.event
# async def update_sprite(sid, data):
#     sprite = Sprite(**data)
#     for i, s in enumerate(sprites):
#         if s.id == sprite.id:
#             sprites[i] = sprite
#             break
#     else:
#         sprites.append(sprite)
#     await sio.emit("update_sprites", sprites)

@sio.event
def update_ui_state(sid, data):
    # global ui_state
    # ui_state = UIState(**data)
    print(data)
    # await sio.emit("update_ui_state", ui_state.dict())

def update_sprites():
    data = [{"type": "robot_yel", "x": -1000, "y": 100, "rotation": 1.57},
            {"type": "robot_blu", "x": 1400, "y": 100, "rotation": 3.14},
            {"type": "ball", "x": 200, "y": 400}]
    sio.emit("update_sprites", data)


# Run the app
if __name__ == "__main__":
    import eventlet
    app = socketio.WSGIApp(sio)
    eventlet.wsgi.server(eventlet.listen(('localhost', 8000)), app)
