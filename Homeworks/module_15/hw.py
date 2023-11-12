import requests

base_url = "https://api.punkapi.com"


def test_get():
    response = requests.get(base_url + "/v2/beers/8")

    expected_abv = 4.7
    expected_name = 'Fake Lager'
    assert response.status_code == 200

    response_dict = response.json()[0]
    assert response_dict['name'] == expected_name
    assert response_dict['abv'] == expected_abv


def test_absent_ednpoint():
    response = requests.delete(base_url + "/v2/beers/8")

    assert response.status_code == 404
    assert "No endpoint found that matches '/v2/beers/8" in response.text
