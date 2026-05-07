import pytest

from parser.core import FreelancehuntParser


@pytest.mark.asyncio
async def test_fetch_html_success(mocker):
    mock_html = "<html><body>Test Jobs</body></html>"
    mock_get = mocker.patch("httpx.AsyncClient.get")

    mock_response = mocker.Mock()
    mock_response.text = mock_html
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    parser = FreelancehuntParser(base_url="https://test.com")

    result = await parser.fetch_html("/jobs")

    mock_get.assert_called_once_with("/jobs")
    assert result == mock_html


def test_parse_jobs_success():
    fake_html = """
    <tr>
        <td class="left">
            <a href="/project/123.html" class="visitable">Розробка Telegram бота на Python</a>
        </td>
        <td class="text-green price">
            5000 грн
        </td>
    </tr>
    """
    parser = FreelancehuntParser(base_url="https://test.com")

    jobs = parser.parse_jobs(fake_html)

    assert len(jobs) == 1
    assert jobs[0]["title"] == "Розробка Telegram бота на Python"
    assert jobs[0]["url"] == "https://test.com/project/123.html"
    assert jobs[0]["budget"] == "5000 грн"
