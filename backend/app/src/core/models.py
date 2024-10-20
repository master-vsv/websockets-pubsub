from enum import Enum

from pydantic import BaseModel


class ChanelTypeEnum(str, Enum):
    system="system"
    user_event="user_event"
    entity_enent="entity_enent"
    schetduller_event="schetduller_event"

class WebsocketMessageContent(BaseModel):
    header: str
    body: str
    object: dict | None


class WebsocketMessage(BaseModel):
    chanel_type: str
    chanel_id: str
    user_id: int
    message: WebsocketMessageContent