import requests


def checking_url(url):
    url_for_check = url.name
    try:
        r = requests.get(url_for_check)
        r.raise_for_status()
        return r.status_code
    except requests.exceptions.RequestException:
        return None