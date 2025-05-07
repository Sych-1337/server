from fastapi import FastAPI
import httpx

app = FastAPI()

KEITARO_CAMPAIGN_URL = "https://firtsoneballs.xyz/XD2gBKJv"

@app.get("/kb")
async def get_offer(user_id: str, campaign: str = "slot01"):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 11; Pixel 5 Build/RQ3A.210805.001.A1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com/",
        }

        async with httpx.AsyncClient(follow_redirects=False) as client:
            response = await client.get(
                KEITARO_CAMPAIGN_URL,
                params={"sub_id": user_id, "campaign": campaign},
                headers=headers
            )

        print(">>> RESPONSE HEADERS:", response.headers)

        if "location" in response.headers:
            return {"status": "ok", "url": response.headers["location"]}
        else:
            return {"status": "game"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
