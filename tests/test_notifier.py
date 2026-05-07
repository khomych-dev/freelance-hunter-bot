from unittest.mock import AsyncMock

import pytest

from services.notifier import TelegramNotifier


@pytest.mark.asyncio
async def test_send_job_calls_send_message_once() -> None:
    bot = type("BotStub", (), {})()
    bot.send_message = AsyncMock()

    notifier = TelegramNotifier(bot=bot, chat_id=123)
    job = {"title": "Test title", "budget": "1000 UAH", "url": "https://example.com/job/1"}

    await notifier.send_job(job)

    bot.send_message.assert_awaited_once_with(
        chat_id=123,
        text="<b>Test title</b>\n<b>Budget:</b> 1000 UAH\n<a href=\"https://example.com/job/1\">Open job</a>",
        parse_mode="HTML",
    )
