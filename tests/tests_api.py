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
TEST_RESULT_DRIVER = [{'name': 'Sebastian Vettel',
                       'abbr': 'SVF',
                       'team': 'FERRARI',
                       'time': '0:01:04.415000'}]


@patch('src.web_report_app.get_drivers')
def test_response_content_json(get_drivers, client):
    get_drivers.return_value = TEST_RESULT
    response = client.get('/api/v1/report/', query_string={'format': 'json'})
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert len(response.json) == 3
    assert response.json[0] == {
        'name': 'Sebastian Vettel',
        'serial number': 1,
        'team': 'FERRARI',
        'time': '0:01:04.415000'}


@patch('src.web_report_app.get_drivers')
def test_response_content_xml(get_drivers, client):
    get_drivers.return_value = TEST_RESULT
    response = client.get('/api/v1/report/', query_string={'format': 'xml'})
    soup = BeautifulSoup(response.data)
    snipet = soup.select('name')
    return_text = 'Sebastian Vettel'
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert len(snipet) == 1
    assert snipet[0].text == return_text


@patch('src.web_report_app.get_drivers')
def test_normal_behavior_report_order_route(get_drivers, client):
    get_drivers.return_value = TEST_RESULT_ORDER
    response = client.get(
        '/api/v1/report/',
        query_string={
            'order': 'desc',
            'format': 'json'})
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert len(response.json) == 3
    assert response.json[0] == {
        'name': 'Stoffel Vandoorne',
        'serial number': 1,
        'team': 'MCLAREN RENAULT',
        'time': '0:01:12.463000'}


@patch('src.web_report_app.get_drivers')
def test_response_content_xml(get_drivers, client):
    get_drivers.return_value = TEST_RESULT_ORDER
    response = client.get(
        '/api/v1/report/',
        query_string={
            'order': 'desc',
            'format': 'xml'})
    soup = BeautifulSoup(response.data)
    snipet = soup.select('name')
    return_text = 'Stoffel Vandoorne'
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert len(snipet) == 3
    assert snipet[0].text == return_text


@patch('src.web_report_app.get_drivers')
def test_normal_behavior_drivers_route_json(get_drivers, client):
    get_drivers.return_value = TEST_RESULT
    response = client.get('/api/v1/drivers/', query_string={'format': 'json'})
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert len(response.json) == 3
    assert response.json[0] == {
        'abbr': 'SVF',
        'name': 'Sebastian Vettel',
        'serial number': 1,
        'team': 'FERRARI'}


@patch('src.web_report_app.get_drivers')
def test_normal_behavior_drivers_route_xml(get_drivers, client):
    get_drivers.return_value = TEST_RESULT
    response = client.get('/api/v1/drivers/', query_string={'format': 'xml'})
    soup = BeautifulSoup(response.data)
    return_text = 'SVF'
    snipet = soup.select('abbr')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert len(snipet) == 3
    assert snipet[0].text == return_text


@patch('src.web_report_app.get_drivers')
def test_normal_behavior_drivers_route_json_order(get_drivers, client):
    get_drivers.return_value = TEST_RESULT_ORDER
    response = client.get(
        '/api/v1/drivers/',
        query_string={
            'format': 'json',
            'order': 'desc'})
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert len(response.json) == 3
    assert response.json[0] == {
        'abbr': 'SVM',
        'name': 'Stoffel Vandoorne',
        'serial number': 1,
        'team': 'MCLAREN RENAULT'}


@patch('src.web_report_app.get_drivers')
def test_normal_behavior_drivers_route_xml_order(get_drivers, client):
    get_drivers.return_value = TEST_RESULT_ORDER
    response = client.get(
        '/api/v1/drivers/',
        query_string={
            'format': 'xml',
            'order': 'desc'})
    soup = BeautifulSoup(response.data)
    return_text = 'SVM'
    snipet = soup.select('abbr')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert len(snipet) == 3
    assert snipet[0].text == return_text


@patch('src.web_report_app.get_drivers')
def test_normal_behavior_driver_route_json(get_drivers, client):
    get_drivers.return_value = TEST_RESULT_DRIVER
    response = client.get(
        '/api/v1/drivers/',
        query_string={
            'format': 'json',
            'driver_id': 'SVF'})
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert len(response.json) == 1
    assert response.json[0] == {
        'name': 'Sebastian Vettel',
        'team': 'FERRARI',
        'time': '0:01:04.415000'}


@patch('src.web_report_app.get_drivers')
def test_normal_behavior_driver_route_xml(get_drivers, client):
    get_drivers.return_value = TEST_RESULT_DRIVER
    response = client.get(
        '/api/v1/drivers/',
        query_string={
            'format': 'xml',
            'driver_id': 'SVF'})
    soup = BeautifulSoup(response.data)
    return_text = 'Sebastian Vettel'
    snipet = soup.select('name')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert len(snipet) == 1
    assert snipet[0].text == return_text


if __name__ == "__main__":
    pytest.main()
