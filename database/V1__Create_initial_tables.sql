-- 確保使用正確的資料庫
USE taiex_analysis;

-- 1. 股票主表
CREATE TABLE IF NOT EXISTS stocks (
    symbol VARCHAR(10) PRIMARY KEY,
    company_name VARCHAR(50) NOT NULL,
    industry VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE
);

-- 2. 歷史日K線表
CREATE TABLE IF NOT EXISTS daily_prices (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    trade_date DATE NOT NULL,
    open_price DECIMAL(10,2) NOT NULL,
    high_price DECIMAL(10,2) NOT NULL,
    low_price DECIMAL(10,2) NOT NULL,
    close_price DECIMAL(10,2) NOT NULL,
    volume BIGINT NOT NULL,
    FOREIGN KEY (symbol) REFERENCES stocks(symbol),
    -- 確保同一天同一檔股票不會重複寫入 (防呆機制)
    UNIQUE KEY unique_symbol_date (symbol, trade_date)
);

-- 3. 新聞與情緒分析表
CREATE TABLE IF NOT EXISTS news_sentiment (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    news_date DATE NOT NULL,
    title VARCHAR(255) NOT NULL,
    sentiment_score DECIMAL(5,4) NOT NULL,
    source_url VARCHAR(500),
    FOREIGN KEY (symbol) REFERENCES stocks(symbol)
);

-- 4. 模型預測結果表
CREATE TABLE IF NOT EXISTS ai_predictions (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    predict_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    action_signal VARCHAR(10) NOT NULL,
    confidence DECIMAL(5,4) NOT NULL,
    FOREIGN KEY (symbol) REFERENCES stocks(symbol)
);