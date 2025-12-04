import validators

def validate_url(url):
    if not validators.url(url) or len(url) > 255:
        return False
    return True