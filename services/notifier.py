from __future__ import annotations

from html import escape
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiogram import Bot


class TelegramNotifier:
    def __init__(self, bot: Bot, chat_id: int | str) -> None:
        self.bot = bot
        self.chat_id = chat_id

    async def send_job(self, job: dict[str, str]) -> None:
        title = escape(job.get("title", ""))
        budget = escape(job.get("budget", ""))
        url = escape(job.get("url", ""), quote=True)

        parts: list[str] = [f"<b>{title}</b>"]
        if budget:
            parts.append(f"<b>Budget:</b> {budget}")
        if url:
            parts.append(f'<a href="{url}">Open job</a>')

        formatted_text = "\n".join(parts)

        await self.bot.send_message(
            chat_id=self.chat_id,
            text=formatted_text,
            parse_mode="HTML",
        )
