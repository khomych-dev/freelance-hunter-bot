import pytest

from parser.core import FreelancehuntParser


@pytest.mark.asyncio
async def test_fetch_html_success(mocker):
    mock_html = "<html><body>Test Jobs</body></html>"

    mock_session_class = mocker.patch("parser.core.AsyncSession")
    mock_session_instance = mock_session_class.return_value.__aenter__.return_value

    mock_response = mocker.Mock()
    mock_response.text = mock_html

    mock_session_instance.get.return_value = mock_response

    parser = FreelancehuntParser()
    result = await parser.fetch_html("/projects")

    assert result == mock_html
    mock_session_instance.get.assert_called_once_with(
        "https://freelancehunt.com/projects"
    )


@pytest.mark.asyncio
async def test_fetch_html_http_error(mocker):
    mock_session_class = mocker.patch("parser.core.AsyncSession")
    mock_session_instance = mock_session_class.return_value.__aenter__.return_value

    mock_response = mocker.Mock()
    mock_response.raise_for_status.side_effect = Exception("HTTP Error")
    mock_session_instance.get.return_value = mock_response

    parser = FreelancehuntParser()

    with pytest.raises(Exception, match="HTTP Error"):
        await parser.fetch_html("/projects")


def test_parse_jobs():
    html = """
    <table>
        <tr>
            <td><a class="visitable" href="/project/123.html">Test Job 1</a></td>
            <td class="price">1000 UAH</td>
        </tr>
        <tr>
            <td><a class="visitable" href="/project/456.html">Test Job 2</a></td>
            </tr>
    </table>
    """
    parser = FreelancehuntParser(base_url="https://test.com")
    jobs = parser.parse_jobs(html)

    assert len(jobs) == 2
    assert jobs[0]["title"] == "Test Job 1"
    assert jobs[0]["url"] == "https://test.com/project/123.html"
    assert jobs[0]["budget"] == "1000 UAH"

    assert jobs[1]["title"] == "Test Job 2"
    assert jobs[1]["url"] == "https://test.com/project/456.html"
    assert jobs[1]["budget"] == ""
