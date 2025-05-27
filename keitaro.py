import httpx
from config import APP_CONFIG

async def get_offer_url(user_id: str, campaign: str, app_name: str) -> str | None:
    app = APP_CONFIG.get(app_name)
    if not app:
        return None

    stream_url = app["keitaro_url"]
    if not stream_url:
        return None

    async with httpx.AsyncClient() as client:
        response = await client.get(stream_url, params={"sub_id": user_id, "campaign": campaign})
        if "show" in response.text.lower():
            return str(response.url)
    return None
