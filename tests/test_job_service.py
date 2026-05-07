import pytest

from services.job_service import JobService


@pytest.mark.asyncio
async def test_get_new_jobs_returns_only_unseen_jobs(mocker) -> None:
    endpoint = "/projects"
    html = "<html></html>"
    parsed_jobs = [
        {
            "title": "First job",
            "url": "https://freelancehunt.com/project/1",
            "budget": "1000",
        },
        {
            "title": "Second job",
            "url": "https://freelancehunt.com/project/2",
            "budget": "2000",
        },
    ]

    parser = mocker.Mock()
    parser.fetch_html = mocker.AsyncMock(return_value=html)
    parser.parse_jobs.return_value = parsed_jobs

    service = JobService(parser=parser)

    first_call_jobs = await service.get_new_jobs(endpoint)
    second_call_jobs = await service.get_new_jobs(endpoint)

    assert first_call_jobs == parsed_jobs
    assert second_call_jobs == []
    assert parser.fetch_html.await_count == 2
    assert parser.parse_jobs.call_count == 2
