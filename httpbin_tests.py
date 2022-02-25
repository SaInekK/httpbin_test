import logging

import requests
import pytest


for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(filename='httpbin_testing.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


headers_list = [{"User-Agent": "Chrome/98.0.4758.102"},
                {"Host": "google.com"},
                {"Accept-Encoding": "gzip, deflate", "Host": "google.com"},
                {"User-Agent": "python-requests/2.27.2"}, ]


@pytest.mark.parametrize('headers', headers_list)
def test_get_headers(headers):
    link = "https://httpbin.org/headers"
    response = requests.get(link, headers=headers)
    logging.debug(f"Request headers: {headers}")
    logging.debug(f"Response: {response.status_code}")
    logging.debug(f"Response headers: {response.headers}")
    assert response.status_code == 200, "Status code != 200"

    # (test_key, test_value), = headers.items()
    response_json = response.json()
    for test_key in headers.keys():
        assert headers[test_key] == response_json['headers'][test_key]


status_codes_list = [*range(101, 104),
                     *range(200, 209), 226,
                     *range(304, 307), *range(308, 309),
                     *range(400, 419), *range(421, 432), 451,
                     *range(500, 512)]


@pytest.mark.parametrize('status', status_codes_list)
def test_get_status(status):
    link = f"https://httpbin.org/status/{status}"
    response = requests.get(link)

    response_status_code = response.status_code
    logging.debug(f"Response: {response.status_code}")
    assert response_status_code == status, "Requested status code != responded status code"
