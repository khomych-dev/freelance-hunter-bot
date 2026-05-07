import asyncio
from unittest.mock import AsyncMock

import pytest

from scheduler.runner import BotRunner


@pytest.mark.asyncio
async def test_runner_run_single_iteration(mocker) -> None:
    job_service = mocker.Mock()
    job_service.get_new_jobs = AsyncMock(
        return_value=[
            {"title": "Job 1", "budget": "100", "url": "https://example.com/1"},
            {"title": "Job 2", "budget": "200", "url": "https://example.com/2"},
        ]
    )

    notifier = mocker.Mock()
    notifier.send_job = AsyncMock()

    mocker.patch("scheduler.runner.asyncio.sleep", side_effect=asyncio.CancelledError)

    runner = BotRunner(
        job_service=job_service,
        notifier=notifier,
        interval_seconds=1,
        endpoint="/projects",
    )

    with pytest.raises(asyncio.CancelledError):
        await runner.run()

    job_service.get_new_jobs.assert_awaited()
    assert notifier.send_job.await_count == 2
