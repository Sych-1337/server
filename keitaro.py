import httpx
from config import KEITARO_URL

async def get_offer_url(user_id: str) -> str | None:
    async with httpx.AsyncClient() as client:
        response = await client.get(KEITARO_URL, params={"sub_id": user_id})
        if "show" in response.text.lower():  # условие подставишь своё
            return "https://your-offer.com"
        return None
