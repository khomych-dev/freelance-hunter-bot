import httpx


class FreelancehuntParser:
    def __init__(self, base_url: str = "https://freelancehunt.com"):
        self.base_url = base_url

    async def fetch_html(self, endpoint: str) -> str:
        async with httpx.AsyncClient(base_url=self.base_url) as client:
            response = await client.get(endpoint)
            response.raise_for_status()
            return response.text
