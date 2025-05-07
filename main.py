from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx

app = FastAPI()

KEITARO_CAMPAIGN_URL = "https://firtesoneballs.xyz/XD2gBKJv"  

@app.get("/kb")
async def get_offer(user_id: str, campaign: str = "kotlinTest"):
    try:
        async with httpx.AsyncClient() as client:
            # Добавляем параметры Keitaro (user_id, campaign и т.д.)
            response = await client.get(
                KEITARO_CAMPAIGN_URL,
                params={"sub_id": user_id, "campaign": campaign},
                follow_redirects=False
            )

            # Получаем редирект
            if "location" in response.headers:
                offer_url = response.headers["location"]
                return {"status": "ok", "url": offer_url}
            else:
                return {"status": "game"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
