# AI 台股走勢預測與分析系統 (AI Stock Prediction System)

## 📝 專案簡介
本專案為一個全端微服務應用，透過歷史台股數據與財經新聞消息面，利用 AI 模型輔助分析最佳的買賣點。系統支援跨平台操作（Web & App 體驗），並提供視覺化的數據儀表板。

## 🏗️ 系統架構與技術棧
本系統採用微服務架構 (Microservices) 進行職責分離：

* **資料與 AI 微服務 (Python)**
    * 使用 `yfinance` / `twstock` 爬取台股 OHLCV 歷史數據。
    * 使用 `BeautifulSoup` 爬取財經新聞進行 NLP 情感分析。
    * 建立預測模型並透過 `FastAPI` 提供輕量化 API。
* **核心業務後端 (Java Spring Boot)**
    * 採用嚴謹的 MVC 架構設計。
    * 負責會員邏輯、資料存取 (Spring Data JPA) 與整合 Python 端之 AI 預測結果。
    * 資料庫：MySQL。
* **跨平台前端 (Angular)**
    * 使用 Angular 打造高互動性單頁應用 (SPA)。
    * 響應式設計 (RWD)，相容桌面與行動裝置瀏覽。

## 📂 目錄結構
* `/data-service` : Python 爬蟲與 AI 模型訓練環境。
* `/backend-service` : Java Spring Boot 後端 API 服務。
* `/frontend-app` : Angular 視覺化介面。
