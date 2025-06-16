import httpx
from config import APP_CONFIG

async def get_offer_url(user_id: str, campaign: str, app_name: str, tracking_id: str = "", sub_ids: dict = {}) -> str | None:
    app = APP_CONFIG.get(app_name)
    if not app:
        return None

    stream_url = app.get("keitaro_url")
    if not stream_url:
        return None

    params = {
        "sub_id": user_id,
        "campaign": campaign,
        "tracking_id": tracking_id
    }

    # Добавим sub_id_2 ... sub_id_8
    for key, value in sub_ids.items():
        if value:
            params[key] = value

    async with httpx.AsyncClient(follow_redirects=False) as client:
        response = await client.get(stream_url, params=params)
        if "location" in response.headers:
            return response.headers["location"]

    return None
