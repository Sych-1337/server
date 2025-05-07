from fastapi import FastAPI
import httpx

app = FastAPI()

KEITARO_CAMPAIGN_URL = "https://firtsoneballs.xyz/XD2gBKJv"  # Убедись, что домен правильный

@app.get("/kb")
async def get_offer(user_id: str, campaign: str = "kotlinTest"):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 Chrome/112.0.0.0 Mobile Safari/537.36"
        }

        async with httpx.AsyncClient(follow_redirects=False) as client:
            response = await client.get(
                KEITARO_CAMPAIGN_URL,
                params={"sub_id": user_id, "campaign": campaign},
                headers=headers
            )

        # Если есть редирект — отдаём ссылку
        if "location" in response.headers:
            return {"status": "ok", "url": response.headers["location"]}
        else:
            return {"status": "game"}  # Иначе — игра
    except Exception as e:
        return {"status": "error", "message": str(e)}
