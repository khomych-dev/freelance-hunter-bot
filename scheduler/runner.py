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
        endpoint: str,
    ) -> None:
        if interval_seconds <= 0:
            raise ValueError("interval_seconds must be greater than zero.")
        if not endpoint:
            raise ValueError("endpoint cannot be empty.")

        self.job_service = job_service
        self.notifier = notifier
        self.interval_seconds = interval_seconds
        self.endpoint = endpoint

    async def run(self) -> None:
        logger.info(
            f"The bot has been launched. Check interval: {self.interval_seconds} seconds."
        )

        while True:
            try:
                new_jobs = await self.job_service.get_new_jobs(endpoint=self.endpoint)
                logger.info(f"Check completed. Found new jobs: {len(new_jobs)}")

                for job in new_jobs:
                    await self.notifier.send_job(job)
            except asyncio.CancelledError:
                logger.info("Runner has been cancelled.")
                raise
            except Exception as e:
                logger.error("Runner iteration failed: {}", e)

            await asyncio.sleep(self.interval_seconds)
