import psycopg2
import os

try:
    from dotenv import load_dotenv
    load_dotenv(".env")
except ModuleNotFoundError:
    pass

DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)


class URL:
    def __init__(self, id, name, created_at):
        self.id = id
        self.name = name
        self.created_at = created_at

    @staticmethod
    def add_to_urls(url):
        try:
            with conn.cursor() as curs:
                curs.execute("INSERT INTO urls (name) VALUES (%s);", (url,))
                conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Ошибка при добавлении URL: {e}")

    @staticmethod
    def get_id(url):
        try:
            with conn.cursor() as curs:
                curs.execute("SELECT id FROM urls WHERE name=%s;", (url,))
                result = curs.fetchone()
                if result:
                    return result[0]
                else:
                    print(f"URL '{url}' не найден.")
                    return None
        except Exception as e:
            print(f"Ошибка при получении ID для URL '{url}': {e}")
            return None

    @staticmethod
    def get_all_urls():
        try:
            with conn.cursor() as curs:
                curs.execute("SELECT * FROM urls ORDER BY created_at DESC;")
                rows = curs.fetchall()
                return [URL(*row) for row in rows]
        except Exception as e:
            print(f"Ошибка при получении всех URL: {e}")
            return []

    @staticmethod
    def get_url(url_id):
        try:
            with conn.cursor() as curs:
                curs.execute("SELECT * FROM urls WHERE id=%s;", (url_id,))
                row = curs.fetchone()
            if row:
                return URL(*row)
            return None
        except Exception as e:
            print(f"Ошибка при получении URL с ID '{url_id}': {e}")
            return None
