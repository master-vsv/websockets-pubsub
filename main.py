from dataclasses import dataclass
from enum import Enum
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
import asyncio

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

websocket_manager: WebSocketManager = WebSocketManager()

class ChanelTypeEnum(str, Enum):
    system="system"
    user_event="user_event"
    entity_enent="entity_enent"
    schetduller_event="schetduller_event"
    
class Message(BaseModel):
    chanel_type: ChanelTypeEnum
    chanel_id: str
    user_id: int
    message: str


@app.websocket("/ws/{chanel_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, chanel_id: str, user_id: int):
    await websocket_manager.add_user_to_chanel(chanel_id, websocket)
    message = Message(
        chanel_type=ChanelTypeEnum.system,
        user_id=user_id,
        chanel_id=chanel_id,
        message=f"User {user_id} connected to chanel - {chanel_id}"
    )
    print("!!!!!!",message.model_dump_json())
    await websocket_manager.broadcast_to_chanel(chanel_id, message.model_dump_json())
    
    try:
        while True:
            await asyncio.sleep(0.1)
            print("tic")
            data = await websocket.receive_text()
            message = Message(
                chanel_type=ChanelTypeEnum.system,
                user_id=user_id,
                chanel_id=chanel_id,
                message=data
            )
            await websocket_manager.send_personal_message(f"You wrote: {message.model_dump_json()}",websocket)
            await websocket_manager.broadcast_to_chanel(chanel_id, message.model_dump_json())

    except WebSocketDisconnect:
        await websocket_manager.remove_user_from_chanel(chanel_id, websocket)
        message = Message(
            chanel_type=ChanelTypeEnum.system,
            user_id=user_id,
            chanel_id=chanel_id,
            message=f"User {user_id} disconnected from chanel - {chanel_id}"
        )
        
        await websocket_manager.broadcast_to_chanel(chanel_id, message.model_dump_json())


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
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, ws_ping_interval=30, ws_ping_timeout=30, workers=2)
    # test_read_main()
    # test_websocket()