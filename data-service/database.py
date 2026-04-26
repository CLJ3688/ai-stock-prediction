import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# 載入 .env 檔案中的環境變數
load_dotenv()

# 獲取資料庫連線資訊
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# 組裝 SQLAlchemy 連線字串 

DATABASE_URL = URL.create(
            drivername="mysql+pymysql",
            username=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=int(DB_PORT) if DB_PORT else 3306,
            database=DB_NAME
)

# # test
# print(f"DB_NAME = {DB_NAME}")
# print(f"database_url = {DATABASE_URL.database}")

# 建立資料庫引擎
engine = create_engine(DATABASE_URL)

def test_connection():
  try:
    # 嘗試連線並執行簡單SQL查詢
    with engine.connect() as connection:
      result = connection.execute(text("SELECT DATABASE();"))
      db_name = result.scalar()
      print(f"成功連線至 MYSQL 資料庫： {db_name}")
  except Exception as e :
    print(f"資料庫連線失敗： {e}")
    
if __name__ == "__main__":
  test_connection()
