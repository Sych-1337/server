from fastapi import FastAPI, Query
from keitaro import get_offer_url
from models import ServerResponse

app = FastAPI()

@app.get("/route-user", response_model=ServerResponse)
async def route_user(user_id: str = Query(...)):
    url = await get_offer_url(user_id)
    if url:
        return ServerResponse(status="ok", url=url)
    return ServerResponse(status="game", url=None)
