from sqlalchemy import text
from db import engine

def test_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("DB Connection OK:", result.fetchone())
    except Exception as e:
        print("DB Connection Error:", e)

if __name__ == "__main__":
    test_connection()
