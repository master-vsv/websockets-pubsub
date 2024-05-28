import argparse
import asyncio
import json
import logging
from dataclasses import dataclass
from enum import Enum

import uvicorn
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from app.src.websocket.websocket_manager import WebSocketManager
from app.src.redis.redis_connect import RedisConnect
from app.src.core.settings import settings

# parser = argparse.ArgumentParser()
# parser.add_argument("-p", "--port", default=8000, type=int)
# args = parser.parse_args()
   
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FastAPI app")

redis_connection = RedisConnect(redis_url=settings.REDIS_URL)
websocket_manager: WebSocketManager = WebSocketManager(redis_connection=redis_connection)
templates = Jinja2Templates(directory="app/src/templates/")

def get_application() -> FastAPI:
    app = FastAPI()

    # Adding the CORS middleware to the app
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.on_event("startup")
    async def startup_event() -> None:
        # await rc.connect()
        redis_connection.is_redis_sync_available()
        redis_connection.is_redis_async_available()
        print('connect')

    

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
        print(chanel_id)
        await websocket_manager.add_websocket_to_chanel(chanel_id, websocket)
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
                #await asyncio.sleep(0.1)
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

        except WebSocketDisconnect as error:
            print(error)
            await websocket_manager.remove_user_from_chanel(chanel_id, websocket)
            message = Message(
                chanel_type=ChanelTypeEnum.system,
                user_id=user_id,
                chanel_id=chanel_id,
                message=f"User {user_id} disconnected from chanel - {chanel_id}"
            )
            
            await websocket_manager.broadcast_to_chanel(chanel_id, message.model_dump_json())


    @app.get("/", response_class=HTMLResponse)
    def read_index(request: Request):
        # Render the HTML template
        return templates.TemplateResponse("index.html", {"request" : request})
    
    return app

app = get_application()

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, ws_ping_interval=30, ws_ping_timeout=30, workers=2)
#     # test_read_main()
#     # test_websocket()