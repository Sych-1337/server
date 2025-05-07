import httpx
from config import CAMPAIGN_STREAMS

async def get_offer_url(user_id: str, campaign: str) -> str | None:
    stream_url = CAMPAIGN_STREAMS.get(campaign)
    if not stream_url:
        return None

    async with httpx.AsyncClient() as client:
        response = await client.get(stream_url, params={"sub_id": user_id})
        if "show" in response.text.lower():  # кастомизируй под кейтаро ответ
            return str(response.url)
    return None
