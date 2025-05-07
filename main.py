from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx
import os

app = FastAPI()

KEITARO_CAMPAIGN_URL = "https://firtsoneballs.xyz/XD2gBKJv"  # проверь, что домен правильный

@app.get("/kb")
async def get_offer(user_id: str, campaign: str = "kotlinTest"):
    try:
        async with httpx.AsyncClient(follow_redirects=False) as client:
            response = await client.get(
                KEITARO_CAMPAIGN_URL,
                params={"sub_id": user_id, "campaign": campaign}
            )

        # Проверяем наличие редиректа
        if "location" in response.headers:
            return {"status": "ok", "url": response.headers["location"]}
        else:
            return {"status": "game"}  # Показываем игру
    except Exception as e:
        return {"status": "error", "message": str(e)}
