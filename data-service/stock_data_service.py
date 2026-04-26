import yfinance as yf
import pandas as pd
from sqlalchemy import text
# 自定義資料庫連線引擎
from database import engine

def add_stock_info(symbol, company_name, industry):
  '''
  step 1 : 確保股票代碼已存於主表中
  '''
  try:
    with engine.connect() as conn:
      query = text("""
                   INSERT IGNORE INTO stocks (symbol, company_name, industry, is_active)
                   VALUES (:symbol, :company_name, :industry, 1)
                   """)
      conn.execute(query, {"symbol" : symbol, "company_name" : company_name, "industry" : industry})
      conn.commit()
      print(f"股票 {symbol} ({company_name}) 已成功儲存")
  except Exception as e:
    print(f"儲存股票資訊時發生錯誤：{e}")
    
def fetch_and_save_daily_prices(symbol, start_date, end_date):
  ''' 
  step 2 : 透過 yfinance 抓取歷史資料，資料清洗後寫入資料庫
  '''
  
  yf_symbol = f"{symbol}.TW"
  print(f"正在抓取 {yf_symbol} 的歷史數據 ( {start_date} 到 {end_date} ) ...")
  
  # 1.抓取資料
  df = yf.download(yf_symbol, start=start_date, end=end_date)
  
  if df.empty:
    print(f"找不到 {symbol} 的數據，請確認代碼或日期範圍。")
    return
  
  # 2.資料清洗
  df = df.reset_index()
  
  if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)
  
  df = df.rename(columns={
        'Date' : 'trade_date',
        'Open' : 'open_price',
        'High' : 'high_price',
        'Low' : 'low_price',
        'Close' : 'close_price',
        'Volume' : 'volume'
  })
  
  df = df[['trade_date', 'open_price', 'high_price', 'low_price', 'close_price', 'volume']].copy()
  df['symbol'] = symbol
  df = df.dropna()
  
  # 3. 寫入資料庫
  try:
    # if_exists='append' 代表接續寫入; index = False 避免寫入 pandas 的流水號
    df.to_sql(name='daily_prices', con=engine, if_exists='append', index=False)
    print(f"成功將 {len(df)} 筆 {symbol} 的歷史股價寫入 daily_prices 資料表")
  except Exception as e:
    print(f"寫入股價資料庫時發生錯誤 {e}")
    
if __name__ == "__main__":
  #hardcode 寫入0050資料
  TARGET_SYMBOL = "0050"
  TARGET_NAME = "元大台灣50"
  TARGET_INDUSTRY = "ETF"
  
  START_DATE = "2024-01-01"
  END_DATE = "2026-04-26"
  
  add_stock_info(TARGET_SYMBOL, TARGET_NAME, TARGET_INDUSTRY)
  fetch_and_save_daily_prices(TARGET_SYMBOL, START_DATE, END_DATE)
