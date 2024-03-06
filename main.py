from dataclasses import dataclass
import logging
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.testclient import TestClient
from src.websocket.websocket_manager import WebSocketManager
import json
import argparse
from pydantic import BaseModel

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", default=8000, type=int)
args = parser.parse_args()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FastAPI app")

app = FastAPI()

# Adding the CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

socket_manager: WebSocketManager = WebSocketManager()

class Message(BaseModel):
    user_id: int
    chanel_id: str
    message: str


@app.websocket("/ws/{chanel_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, chanel_id: str, user_id: int):
    await socket_manager.add_user_to_chanel(chanel_id, websocket)
    message = Message(
        user_id=user_id,
        chanel_id=chanel_id,
        message=f"User {user_id} connected to chanel - {chanel_id}"
    )
    
    await socket_manager.broadcast_to_chanel(chanel_id, message.model_dump_json())
    try:
        while True:
            data = await websocket.receive_text()
            message = Message(
                user_id=user_id,
                chanel_id=chanel_id,
                message=data
            )
           
            await socket_manager.broadcast_to_chanel(chanel_id, message.model_dump_json())

    except WebSocketDisconnect:
        await socket_manager.remove_user_from_chanel(chanel_id, websocket)
        message = Message(
            user_id=user_id,
            chanel_id=chanel_id,
            message=f"User {user_id} disconnected from chanel - {chanel_id}"
        )
        
        await socket_manager.broadcast_to_chanel(chanel_id, message.model_dump_json())


templates = Jinja2Templates(directory="src/templates")

@app.get("/", response_class=HTMLResponse)
def read_index(request: Request):
    # Render the HTML template
    return templates.TemplateResponse("index.html", {"request" : request})


def test_read_main():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_websocket():
    client = TestClient(app)
    with client.websocket_connect("/ws/1/1") as websocket:
        data = websocket.receive_json()
        assert data == {"msg": "Hello WebSocket"}
        

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=args.port, reload=True)
    test_read_main()
    test_websocket()