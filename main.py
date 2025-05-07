from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx
import os

app = FastAPI()

KEITARO_CAMPAIGN_URL = "https://firtsoneballs.xyz/XD2gBKJv"  # Убедись, что домен без ошибок

@app.get("/kb")
async def get_offer(request: Request, user_id: str, campaign: str = "kotlinTest"):
    try:
        # Логируем заголовки (для отладки фильтров Keitaro)
        headers = dict(request.headers)
        print(">>> User-Agent:", headers.get("user-agent"))
        print(">>> X-Forwarded-For:", headers.get("x-forwarded-for"))
        print(">>> IP:", request.client.host)

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
