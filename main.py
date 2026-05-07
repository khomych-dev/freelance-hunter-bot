import asyncio

from aiogram import Bot

from config.settings import Settings
from parser.core import FreelancehuntParser
from scheduler.runner import BotRunner
from services.job_service import JobService
from services.notifier import TelegramNotifier


async def main() -> None:
    settings = Settings()

    bot = Bot(token=settings.TELEGRAM_TOKEN)
    try:
        parser = FreelancehuntParser(base_url=settings.FREELANCEHUNT_URL)
        job_service = JobService(parser=parser)
        notifier = TelegramNotifier(bot=bot, chat_id=settings.TELEGRAM_CHAT_ID)
        runner = BotRunner(
            job_service=job_service,
            notifier=notifier,
            interval_seconds=settings.PARSE_INTERVAL_SECONDS,
        )

        await runner.run()
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())

def main():
    print("Hello from freelance-hunter-bot!")


if __name__ == "__main__":
    main()
