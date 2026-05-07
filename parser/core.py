from urllib.parse import urljoin

from bs4 import BeautifulSoup
from curl_cffi.requests import AsyncSession


class FreelancehuntParser:
    def __init__(self, base_url: str = "https://freelancehunt.com") -> None:
        self.base_url = base_url.rstrip("/")

    async def fetch_html(self, endpoint: str) -> str:
        if not endpoint:
            raise ValueError("Endpoint cannot be empty.")

        full_url = urljoin(f"{self.base_url}/", endpoint.lstrip("/"))

        async with AsyncSession(impersonate="chrome120", timeout=30) as session:
            response = await session.get(full_url)
            response.raise_for_status()
            return response.text

    def parse_jobs(self, html: str) -> list[dict[str, str]]:
        soup = BeautifulSoup(html, "lxml")
        jobs: list[dict[str, str]] = []

        for row in soup.find_all("tr"):
            title_elem = row.find("a", class_="visitable")
            budget_elem = row.find("td", class_="price")

            if title_elem is None:
                continue

            title = title_elem.get_text(strip=True)
            href = title_elem.get("href", "").strip()
            if not title or not href:
                continue

            url = urljoin(f"{self.base_url}/", href)
            budget = budget_elem.get_text(strip=True) if budget_elem else ""

            jobs.append({"title": title, "url": url, "budget": budget})

        return jobs
