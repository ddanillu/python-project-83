import requests
from bs4 import BeautifulSoup


def checking_url(url):
    """
    Проверяет доступность указанного URL и извлекает его метаданные.

    Параметры:
    - url: объект с атрибутом `name`, содержащим URL-строку (например, url.name = 'https://example.com').

    Возвращаемые значения:
    - Возвращает словарь, содержащий:
        - 'code': HTTP статус код (int).
        - 'h1': содержимое тега <h1> (str), или пустую строку, если тег отсутствует.
        - 'title': содержимое тега <title> (str), или пустую строку, если тег отсутствует.
        - 'meta_description': содержимое мета-тега description (str), или пустую строку, если тег отсутствует.
    - Если возникает ошибка при запросе, возвращает None.
    
    Пример использования:
    url = URL(name='https://example.com')
    result = checking_url(url)
    return {'code': 200, 'h1': 'Example Domain', 'title': 'Example', 'meta_description': 'This domain is for use in illustrative examples.'}
    """
    url_for_check = url.name
    headers = {
        'User-Agent': 'Page Analyzer Bot'
    }
    try:
        r = requests.get(url_for_check, headers=headers, timeout=10)
        r.raise_for_status()

        soup = BeautifulSoup(r.content, 'html.parser')
        h1_content = soup.find('h1').text if soup.find('h1') else ""
        title_content = soup.title.string if soup.find('title') else ""
        meta_description = soup.find('meta', attrs={'name': 'description'})
        meta_content = meta_description['content'] if meta_description else ""

        data = {
            'code': r.status_code,
            'h1': h1_content,
            'title': title_content,
            'meta_description': meta_content
        }

        return data
    except requests.exceptions.RequestException:
        return None