from pydantic import BaseModel


class NotificationCreate(BaseModel):

    title: str
    message: str
    receiver: str
    type: str