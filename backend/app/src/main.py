
import asyncio

from app.src.core.logging import logger
from app.src.core.models import ChanelTypeEnum, WebsocketMessage, WebsocketMessageContent
from app.src.core.settings import settings
from app.src.redis.redis_connect import RedisConnect
from app.src.websocket.websocket_manager import WebSocketManager
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

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
        redis_connection.is_redis_sync_available()
        await redis_connection.is_redis_async_available()
        logger.info("App started")

    

    @app.websocket("/ws/{chanel_id}/{user_id}")
    async def websocket_endpoint(websocket: WebSocket, chanel_id: str, user_id: int, chanel_type: str = "system"):
        logger.info(f"websocket_endpoint got {chanel_id}, {user_id}, {chanel_type}, {websocket}")
        await websocket_manager.add_websocket_to_chanel(chanel_id, websocket)
        websocket_message = WebsocketMessage(
            chanel_type=chanel_type,
            user_id=user_id,
            chanel_id=chanel_id,
            message=WebsocketMessageContent(
                header="connect",
                body= f"User {user_id} connected to chanel - {chanel_id}",
                object = None
                )
        )

        await websocket_manager.broadcast_to_chanel(chanel_id, websocket_message)
        logger.info(f"websocket_endpoint broadcast_to_chanel {chanel_id}, {websocket_message}")
        
        try:
            while True:
                await asyncio.sleep(0.1)
                print("tic")
                data = await websocket.receive_text()
                websocket_message = WebsocketMessage(
                    chanel_type=ChanelTypeEnum.system,
                    user_id=user_id,
                    chanel_id=chanel_id,
                    message=WebsocketMessageContent(
                        header="data",
                        body= data,
                        object = None
                        )
                )
                await websocket_manager.send_personal_message(websocket_message, websocket)
                logger.info(f"websocket_endpoint send_personal_message {chanel_id}, {websocket_message}")
                await websocket_manager.broadcast_to_chanel(chanel_id, websocket_message)
                logger.info(f"websocket_endpoint send broadcast_to_chanel {chanel_id}, {websocket_message.model_dump_json()}")

        except WebSocketDisconnect as error:
            logger.error(f"WebSocketDisconnect {error}")
            await websocket_manager.remove_websocket_from_chanel(chanel_id, websocket)
            websocket_message = WebsocketMessage(
                chanel_type=ChanelTypeEnum.system,
                user_id=user_id,
                chanel_id=chanel_id,
                message=WebsocketMessageContent(
                        header="disconnected",
                        body= f"User {user_id} disconnected from chanel - {chanel_id}",
                        object = None
                        )
            )
            
            await websocket_manager.broadcast_to_chanel(chanel_id, websocket_message)
            logger.info(f"websocket_endpoint send disconnected broadcast_to_chanel {chanel_id}, {websocket_message}")


    @app.get("/", response_class=HTMLResponse)
    def read_index(request: Request):
        # Render the HTML template
        return templates.TemplateResponse("index.html", {"request" : request})
    
    @app.get("/send_broadcast_message")
    async def send_broadcast_message(chanel_id: str, message: str):
        websocket_message = WebsocketMessage(
            chanel_type=ChanelTypeEnum.system,
            chanel_id=chanel_id,
            user_id=0,
            message=WebsocketMessageContent(
                            header="broadcast_message",
                            body= message,
                            object = None
                            )
        )
        await websocket_manager.broadcast_to_chanel(chanel_id, websocket_message)
        return websocket_message.model_dump_json()
    return app

app = get_application()

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, ws_ping_interval=30, ws_ping_timeout=30, workers=2)
#     # test_read_main()
#     # test_websocket()