import requests

from pybnafar.downloader import BnafarDownloader


def test_fetch_sources_api_success(mocker):
    # Mocking requests.Session.get for CKAN API
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "result": {
            "resources": [
                {"name": "Test Resource", "url": "http://test.com/data.csv", "format": "csv"}
            ]
        }
    }

    mock_session = mocker.MagicMock()
    mock_session.get.return_value = mock_response
    mock_session.__enter__.return_value = mock_session
    mocker.patch("requests.Session", return_value=mock_session)

    dl = BnafarDownloader(workspace_dir="tmp_test")
    sources = dl.fetch_sources(use_api=True)

    assert len(sources) == 1
    assert sources[0]["title"] == "Test Resource"


def test_fetch_sources_fallback(mocker):
    # Mocking API failure then success on scraping
    mock_api_resp = mocker.MagicMock()
    mock_api_resp.status_code = 500
    mock_api_resp.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Error")

    mock_scrap_resp = mocker.MagicMock()
    mock_scrap_resp.status_code = 200
    mock_scrap_resp.content = (
        b'<li class="resource-item"><a class="heading" title="Scraped Resource"></a>'
        b'<a class="resource-url-analytics" href="http://scraped.com/data.csv"></a></li>'
    )

    # Mock Session for API
    mock_session = mocker.MagicMock()
    mock_session.get.return_value = mock_api_resp
    mock_session.__enter__.return_value = mock_session
    mocker.patch("requests.Session", return_value=mock_session)

    # Mock direct requests.get for Scraping
    mocker.patch("requests.get", return_value=mock_scrap_resp)

    dl = BnafarDownloader(workspace_dir="tmp_test")
    sources = dl.fetch_sources(use_api=True)

    assert len(sources) == 1
    assert sources[0]["title"] == "Scraped Resource"


def test_fetch_sources_total_failure(mocker):
    # Mocking both API and Scraping failures
    mocker.patch(
        "requests.Session.get",
        side_effect=requests.exceptions.ConnectionError("Connection Failed"),
    )
    mocker.patch(
        "requests.get",
        side_effect=requests.exceptions.ConnectionError("Connection Failed"),
    )

    dl = BnafarDownloader(workspace_dir="tmp_test")

    # Should return empty list gracefully and log warning instead of crashing
    sources = dl.fetch_sources(use_api=True)
    assert sources == []
