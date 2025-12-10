import os
from psycopg2 import pool

try:
    from dotenv import load_dotenv
    load_dotenv(".env")
except ModuleNotFoundError:
    pass

class DatabaseManager:
    def __init__(self):
        self.connection_pool = pool.SimpleConnectionPool(1, 10, dsn=os.getenv('DATABASE_URL'))

    def get_connection(self):
        return self.connection_pool.getconn()

    def return_connection(self, conn):
        self.connection_pool.putconn(conn)

    def close(self):
        self.connection_pool.closeall()

db_manager = DatabaseManager()

class URL:
    def __init__(self, id, name, created_at):
        self.id = id
        self.name = name
        self.created_at = created_at

    @staticmethod
    def add_url_and_get_id(url):
        conn = db_manager.get_connection()
        try:
            with conn.cursor() as curs:
                curs.execute("INSERT INTO urls (name) VALUES (%s) RETURNING id;", (url,))
                url_id = curs.fetchone()[0]
                conn.commit()
                return url_id
        except Exception as e:
            conn.rollback()
            print(f"Ошибка при добавлении URL: {e}")
            return None
        finally:
            db_manager.return_connection(conn)


    @staticmethod
    def url_exists(url):
        conn = db_manager.get_connection()
        try:
            with conn.cursor() as curs:
                curs.execute("SELECT EXISTS (SELECT id FROM urls WHERE name = %s);", (url,))
                existing_id = curs.fetchone()[0]
                return existing_id
        except Exception as e:
            print(f"Ошибка при проверке существования URL '{url}': {e}")
            return False
        finally:
            db_manager.return_connection(conn)


    @staticmethod
    def clear_old_urls():
        conn = db_manager.get_connection()
        try:
            with conn.cursor() as curs:
                curs.execute("DELETE FROM urls WHERE created_at < NOW() - INTERVAL '1 day';")
                conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Ошибка при очистке старых URL: {e}")
        finally:
            db_manager.return_connection(conn)


    @staticmethod
    def get_all_urls():
        URL.clear_old_urls()
        conn = db_manager.get_connection() 
        try:
            with conn.cursor() as curs:
                curs.execute("SELECT * FROM urls ORDER BY created_at DESC, id DESC;")
                rows = curs.fetchall()
                return [URL(*row) for row in rows]
        except Exception as e:
            print(f"Ошибка при получении всех URL: {e}")
            return []
        finally:
            db_manager.return_connection(conn)

    @staticmethod
    def get_url(url_id):
        conn = db_manager.get_connection() 
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
        finally:
            db_manager.return_connection(conn)

    
    @staticmethod
    def add_check(url_id, status_code, h1="", title="", description=""):
        conn = db_manager.get_connection()
        try:
            with conn.cursor() as curs:
                curs.execute("""
                    INSERT INTO url_checks (url_id, status_code, h1, title, description) 
                    VALUES (%s, %s, %s, %s, %s);
                """, (url_id, status_code, h1, title, description))
                conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Ошибка при добавлении проверки для URL ID '{url_id}': {e}")
        finally:
            db_manager.return_connection(conn)



    @staticmethod
    def get_checks(url_id):
        conn = db_manager.get_connection()
        try:
            with conn.cursor() as curs:
                curs.execute("SELECT * FROM url_checks WHERE url_id = %s ORDER BY created_at DESC, id DESC;", (url_id,))
                rows = curs.fetchall()
                return [{
                    'id': row[0],
                    'status_code': row[2],
                    'h1': row[3],
                    'title': row[4],
                    'description': row[5],
                    'created_at': row[6]
                } for row in rows]
        except Exception as e:
            print(f"Ошибка при получении проверок для URL ID '{url_id}': {e}")
            return []
        finally:
            db_manager.return_connection(conn)
