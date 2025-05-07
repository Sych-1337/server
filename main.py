from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx

app = FastAPI()

KEITARO_CAMPAIGN_URL = "https://firtsoneballs.xyz/XD2gBKJv"

MOBILE_USER_AGENT = (
    "Mozilla/5.0 (Linux; Android 11; Mobile) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/97.0.0.0 Mobile Safari/537.36"
)

@app.get("/kb")
async def get_offer(request: Request, user_id: str, campaign: str = "kotlinTest"):
    try:
        client_ip = request.headers.get("x-forwarded-for", request.client.host)

        headers = {
            "User-Agent": MOBILE_USER_AGENT,
            "X-Forwarded-For": client_ip
        }

        async with httpx.AsyncClient(follow_redirects=False) as client:
            response = await client.get(
                KEITARO_CAMPAIGN_URL,
                params={"sub_id": user_id, "campaign": campaign},
                headers=headers
            )

        if "location" in response.headers:
            return {"status": "ok", "url": response.headers["location"]}
        else:
            return {"status": "game"}

    except Exception as e:
        return {"status": "error", "message": str(e)}
