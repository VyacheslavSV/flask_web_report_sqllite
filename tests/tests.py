import pytest

from bs4 import BeautifulSoup
from mock import patch

TEST_RESULT = [{'name': 'Sebastian Vettel',
                'abbr': 'SVF',
                'team': 'FERRARI',
                'time': '0:01:04.415000'},
               {'name': 'Valtteri Bottas',
                'abbr': 'VBM',
                'team': 'MERCEDES',
                'time': '0:01:12.434000'},
               {'name': 'Stoffel Vandoorne',
                'abbr': 'SVM',
                'team': 'MCLAREN RENAULT',
                'time': '0:01:12.463000'}]
TEST_RESULT_ORDER = [{'name': 'Stoffel Vandoorne',
                      'abbr': 'SVM',
                      'team': 'MCLAREN RENAULT',
                      'time': '0:01:12.463000'},
                     {'name': 'Valtteri Bottas',
                      'abbr': 'VBM',
                      'team': 'MERCEDES',
                      'time': '0:01:12.434000'},
                     {'name': 'Sebastian Vettel',
                      'abbr': 'SVF',
                      'team': 'FERRARI',
                      'time': '0:01:04.415000'}]
TEST_RESULT_DRIVERS = [{'abbr': 'SVF', 'name': 'Sebastian Vettel'}, {
    'abbr': 'VBM', 'name': 'Valtteri Bottas'}, {'abbr': 'SVM', 'name': 'Stoffel Vandoorne'}]
TEST_RESULT_DRIVERS_ORDER = [{'abbr': 'SVM', 'name': 'Stoffel Vandoorne'}, {
    'abbr': 'VBM', 'name': 'Valtteri Bottas'}, {'abbr': 'SVF', 'name': 'Sebastian Vettel'}]
TEST_RESULT_DRIVER = [{'name': 'Sebastian Vettel',
                       'abbr': 'SVF',
                       'team': 'FERRARI',
                       'time': '0:01:04.415000'}]


@patch('src.web_report_app.get_drivers')
def test_normal_behavior_report_route(get_drivers, client):
    get_drivers.return_value = TEST_RESULT
    response = client.get('/report/')
    soup = BeautifulSoup(response.data, 'html.parser')
    snipet = soup.select('ol > li')
    assert response.status_code == 200
    assert len(snipet) == 3
    assert snipet[0].text == 'Sebastian Vettel FERRARI\n0:01:04.415000\n'


@patch('src.web_report_app.get_drivers')
def test_normal_behavior_report_order_route(get_drivers, client):
    get_drivers.return_value = TEST_RESULT_ORDER
    response = client.get('/report/', query_string={'order': 'desc'})
    soup = BeautifulSoup(response.data, 'html.parser')
    snipet = soup.select('ol > li')
    assert response.status_code == 200
    assert len(snipet) == 3
    assert snipet[0].text == 'Stoffel Vandoorne MCLAREN RENAULT\n0:01:12.463000\n'


@patch('src.web_report_app.get_drivers')
def test_normal_behavior_drivers_route(get_drivers, client):
    get_drivers.return_value = TEST_RESULT_DRIVERS
    response = client.get('/drivers/')
    soup = BeautifulSoup(response.data, 'html.parser')
    snipet = soup.select('ol > li')
    assert response.status_code == 200
    assert len(snipet) == 3
    assert snipet[0].text == '\nSVF\nSebastian Vettel\n'


@patch('src.web_report_app.get_drivers')
def test_normal_behavior_drivers_order_route(get_drivers, client):
    get_drivers.return_value = TEST_RESULT_DRIVERS_ORDER
    response = client.get('/drivers/', query_string={'order': 'desc'})
    soup = BeautifulSoup(response.data, 'html.parser')
    snipet = soup.select('ol > li')
    assert response.status_code == 200
    assert len(snipet) == 3
    assert snipet[0].text == '\nSVM\nStoffel Vandoorne\n'


@patch('src.web_report_app.get_drivers')
def test_normal_behavior_drivers_driver_id_route(get_drivers, client):
    get_drivers.return_value = TEST_RESULT_DRIVER
    response = client.get('/drivers/', query_string={'driver_id': 'SVF'})
    soup = BeautifulSoup(response.data, 'html.parser')
    snipet = soup('body')
    assert response.status_code == 200
    assert len(snipet) == 1
    assert snipet[0].text == '\nSebastian Vettel FERRARI 0:01:04.415000\n'


if __name__ == "__main__":
    pytest.main()
