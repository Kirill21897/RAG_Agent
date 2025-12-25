# scripts/test_db.py
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from config.settings import DATABASE_URL

def test_connection():
    print("Подключаюсь к БД...")
    engine = create_engine(DATABASE_URL)
    try:
        with engine.connect() as conn:
            # Проверка версии и БД
            row = conn.execute(text("SELECT version(), current_database()")).fetchone()
            print(f"Подключено к БД: {row[1]}")
            print(f"PostgreSQL: {row[0].split(' on ')[0]}")

            # Проверка pgvector
            ext = conn.execute(text("SELECT extname FROM pg_extension WHERE extname = 'vector'")).fetchone()
            if ext:
                print("pgvector расширение активно")
            else:
                print("pgvector НЕ найден — проверьте образ!")
                return False
        return True
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return False

if __name__ == "__main__":
    test_connection()