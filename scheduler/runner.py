import asyncio

from loguru import logger

from services.job_service import JobService
from services.notifier import TelegramNotifier


class BotRunner:
    def __init__(
        self,
        job_service: JobService,
        notifier: TelegramNotifier,
        interval_seconds: int,
    ) -> None:
        self.job_service = job_service
        self.notifier = notifier
        self.interval_seconds = interval_seconds

    async def run(self) -> None:
        logger.info(
            f"The bot has been launched. Check interval: {self.interval_seconds} seconds."
        )

        while True:
            try:
                endpoint = "/projects?skills%5B0%5D=1&skills%5B1%5D=22&skills%5B2%5D=99"
                new_jobs = await self.job_service.get_new_jobs(endpoint=endpoint)
                logger.info(f"Check completed. Found new jobs: {len(new_jobs)}")

                for job in new_jobs:
                    await self.notifier.send_job(job)
            except Exception as e:
                logger.error("Runner iteration failed: {}", e)

            await asyncio.sleep(self.interval_seconds)
