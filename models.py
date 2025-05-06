from pydantic import BaseModel

class ServerResponse(BaseModel):
    status: str
    url: str | None
