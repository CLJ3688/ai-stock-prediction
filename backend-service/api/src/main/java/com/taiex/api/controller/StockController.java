package com.taiex.api.controller;

import com.taiex.api.model.Stock;
import com.taiex.api.repository.StockRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/stocks")
public class StockController {
    private final StockRepository stockRepository;

    @Autowired
    public StockController(StockRepository stockRepository){
        this.stockRepository = stockRepository;
    }

    /**
     * API 1: 取得所有股票清單
     * 請求方式: GET http://localhost:8080/api/stocks
     */

    @GetMapping
    public List<Stock> getAllStocks() {
        return stockRepository.findAll();
    }
}
