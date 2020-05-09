import urllib.parse as urlparse
from urllib.parse import urlencode


def add_parameter_to_url(url: str, params: dict) -> str:
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)

    url_parts[4] = urlencode(query)
    return urlparse.urlunparse(url_parts)


if __name__ == '__main__':
    url = "http://127.0.0.1:8000/contact?questioner-email=adf&language=English"
    params = {"state": 0}
    print(add_parameter_to_url(url, params))