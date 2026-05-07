package com.taiex.api.controller;

import com.taiex.api.model.NewsSentiment;
import com.taiex.api.repository.NewsSentimentRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("api/stocks/{symbol}/news")
public class NewsSentimentController {
    private final NewsSentimentRepository newsSentimentRepository;

    @Autowired
    public NewsSentimentController(NewsSentimentRepository newsSentimentRepository) {
        this.newsSentimentRepository = newsSentimentRepository;
    }

    /**
     * 取得特定股票的相關新聞與 AI 情緒分數 (依日期由新到舊排序)
     * GET http://localhost:8080/api/stocks/0050/news
     */

    @GetMapping
    public List<NewsSentiment> getStockNews(@PathVariable String symbol) {
        return newsSentimentRepository.findByStockSymbolOrderByNewsDateDesc(symbol);
    }
}
