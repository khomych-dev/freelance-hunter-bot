from parser.core import FreelancehuntParser


class JobService:
    def __init__(self, parser: FreelancehuntParser) -> None:
        self.parser = parser
        self.seen_urls: set[str] = set()

    async def get_new_jobs(self, endpoint: str) -> list[dict[str, str]]:
        html = await self.parser.fetch_html(endpoint)
        jobs = self.parser.parse_jobs(html)

        new_jobs: list[dict[str, str]] = []
        for job in jobs:
            job_url = job["url"]
            if job_url not in self.seen_urls:
                self.seen_urls.add(job_url)
                new_jobs.append(job)

        return new_jobs
