import pytest
import requests
from pybnafar.downloader import BnafarDownloader

def test_fetch_sources_api_success(mocker):
    # Mocking requests.get for CKAN API
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'result': {
            'resources': [
                {'name': 'Test Resource', 'url': 'http://test.com/data.csv', 'format': 'csv'}
            ]
        }
    }
    mocker.patch('requests.get', return_value=mock_response)
    
    dl = BnafarDownloader(workspace_dir='tmp_test')
    sources = dl.fetch_sources(use_api=True)
    
    assert len(sources) == 1
    assert sources[0]['title'] == 'Test Resource'

def test_fetch_sources_fallback(mocker):
    # Mocking API failure then success on scraping
    mock_api_resp = mocker.Mock()
    mock_api_resp.status_code = 500
    
    mock_scrap_resp = mocker.Mock()
    mock_scrap_resp.status_code = 200
    mock_scrap_resp.content = b'<li class="resource-item"><a class="heading" title="Scraped Resource"></a><a class="resource-url-analytics" href="http://scraped.com/data.csv"></a></li>'
    
    mocker.patch('requests.get', side_effect=[mock_api_resp, mock_scrap_resp])
    
    dl = BnafarDownloader(workspace_dir='tmp_test')
    sources = dl.fetch_sources(use_api=True)
    
    assert len(sources) == 1
    assert sources[0]['title'] == 'Scraped Resource'
