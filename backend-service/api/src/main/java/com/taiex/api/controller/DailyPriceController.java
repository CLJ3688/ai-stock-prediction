package com.taiex.api.controller;

import com.taiex.api.model.DailyPrice;
import com.taiex.api.repository.DailyPriceRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/stocks/{symbol}/prices")
public class DailyPriceController {
    private final DailyPriceRepository dailyPriceRepository;

    @Autowired
    public DailyPriceController(DailyPriceRepository dailyPriceRepository){
        this.dailyPriceRepository = dailyPriceRepository;
    }

    /**
     * API 1: Get historical price of specific stock
     * GET http://localhost:8080/api/stocks/0050/prices
     */

    @GetMapping
    public List<DailyPrice> getStockPrices(@PathVariable String symbol) {
        return dailyPriceRepository.findByStockSymbolOrderByTradeDateDesc(symbol);
    }
}
