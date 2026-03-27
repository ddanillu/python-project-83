import requests
from bs4 import BeautifulSoup


def truncate(text, max_len):
    if len(text) > max_len:
        return text[:max_len-3] + '...'
    return text


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
        h1_tag = soup.find('h1')
        h1_full = h1_tag.text.strip() if h1_tag and h1_tag.text else ""

        title_tag = soup.find('title')
        title_full = title_tag.string.strip() if title_tag and title_tag.string else ""

        meta_description = soup.find('meta', attrs={'name': 'description'})
        desc_full = (meta_description['content'].strip() 
                    if meta_description and meta_description.get('content') else "")

        h1_content = truncate(h1_full,200)
        title_content = truncate(title_full, 200)
        meta_content = truncate(desc_full, 200)

        data = {
            'code': r.status_code,
            'h1': h1_content,
            'title': title_content,
            'meta_description': meta_content
        }

        return data
    except requests.exceptions.RequestException:
        return None