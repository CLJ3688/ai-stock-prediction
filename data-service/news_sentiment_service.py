import requests
from bs4 import BeautifulSoup
from snownlp import SnowNLP
import pandas as pd
from datetime import datetime
from database import engine
from sqlalchemy import text

def fetch_and_analyze_news(symbol, company_name):
  '''
  透過 Google News RSS 抓取特定股票近期新聞，並進行分析
  '''
  
  print(f"正在搜尋 {symbol} {company_name} 的最新新聞...")
  
  # 組合 Google News RSS 搜尋網址
  query = f"{symbol} {company_name}"
  rss_url = f"https://news.google.com/rss/search?q={query} when:7d&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
  
  try:
    # 發送請求取得 XML 資料
    response = requests.get(rss_url)
    response.raise_for_status()
    
    # 使用BeautifulSoup 解析
    soup = BeautifulSoup(response.text, "xml")
    items = soup.find_all("item")
    
    news_data = []
    for item in items:
      title_tag = item.find("title")
      link_tag = item.find("link")
      pub_date_tag = item.find("pubDate")
      
      if not title_tag or not link_tag or not pub_date_tag:
        print("格式缺少，已跳過...")
        
      title = title_tag.text
      link = link_tag.text
      
      # RSS的pubDate 格式轉換為資料庫 DATE 格式
      pub_date_str = pub_date_tag.text

      try:
        pub_date = datetime.strptime(pub_date_str, "%a, %d %b %Y %H:%M:%S GMT").strftime("%Y-%m-%d")
      except Exception as e:
        print(f"日期格式轉換失敗 : {e}")
        continue
      
      # 核心：使用SnowNLP進行分析
      try:
        s = SnowNLP(title)
        sentiment_score = round(s.sentiments, 4)
      except Exception as e:
        print(f"分析失敗 ({title}) : {e}")
        sentiment_score = 0.5000 # 分析失敗給予中位數
      news_data.append({
                  "symbol" : symbol,
                  "news_date" : pub_date,
                  "title" : title,
                  "sentiment_score" : sentiment_score,
                  "source_url" : link
      })
    return pd.DataFrame(news_data)
  except Exception as e:
    print(f"抓取新聞時發生錯誤 : {e}")
    return pd.DataFrame()

def save_news_to_db(df):
  '''
  將分析完的新聞寫入資料庫
  '''
  
  if df.empty:
    print("沒有找到相關新聞可以寫入資料庫")
    return
  
  df = df.drop_duplicates(subset=['title'])
  
  print(f"準備寫入資料庫的資料筆數 : {len(df)}")
  try:
    # 將資料寫入 news_sentiment Table
    df.to_sql(name='news_sentiment', con=engine, if_exists='append', index=False)
    print(f"成功將 {len(df)} 筆新聞與情緒分數寫入資料庫")
  except Exception as e:
    print(f"寫入資料庫時發生錯誤 : {e}")
    
if __name__ == "__main__":
  TARGET_SYMBOL = "0050"
  TARGET_NAME = "元大台灣50"
  
  #執行抓取新聞與分析
  news_df = fetch_and_analyze_news(TARGET_SYMBOL, TARGET_NAME)
  
  if not news_df.empty:
    #印出前五筆資料預覽
    print("\n 分析結果預覽 : ")
    print(news_df[['news_date', 'sentiment_score', 'title']].head())
    print('=' * 50)
    
    #存入資料庫
    save_news_to_db(news_df)
  
  