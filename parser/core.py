from typing import Dict, List

import httpx
from bs4 import BeautifulSoup


class FreelancehuntParser:
    def __init__(self, base_url: str = "https://freelancehunt.com"):
        self.base_url = base_url

    async def fetch_html(self, endpoint: str) -> str:
        async with httpx.AsyncClient(base_url=self.base_url) as client:
            response = await client.get(endpoint)
            response.raise_for_status()
            return response.text

    def parse_jobs(self, html: str) -> List[Dict[str, str]]:
        soup = BeautifulSoup(html, "lxml")
        jobs = []

        rows = soup.find_all("tr")

        for row in rows:
            title_elem = row.find("a", class_="visitable")
            budget_elem = row.find("td", class_="price")

            if title_elem:
                title = title_elem.text.strip()
                url = f"{self.base_url}{title_elem['href']}"

                budget = ""
                if budget_elem:
                    budget = budget_elem.text.strip()

                jobs.append({"title": title, "url": url, "budget": budget})

        return jobs
