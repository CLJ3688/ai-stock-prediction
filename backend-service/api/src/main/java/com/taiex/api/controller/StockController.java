package com.taiex.api.controller;

import com.taiex.api.model.Stock;
import com.taiex.api.repository.StockRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

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

    /**
     * API 2: 查詢單一股票(透過代碼)
     * GET http://localhost:8080/api/stocks/0050
     */

    @GetMapping("/{symbol}")
    public ResponseEntity<Stock> getStockBySymbol(@PathVariable String symbol) {
        return stockRepository.findById(symbol)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    /**
     * API 3:新增股票
     * POST http://localhost:8080/api/stocks
     */

    @PostMapping
    public Stock createStock(@RequestBody Stock stock) {
        return stockRepository.save(stock);
    }

    /**
     * API 4: 更新股票資訊
     * PUT http://localhost:8080/api/stocks/0050
     */

    @PutMapping("/{symbol}")
    public ResponseEntity<Stock> updateStock(@PathVariable String symbol, @RequestBody Stock stockDetails) {
        return stockRepository.findById(symbol)
                .map(existingStock -> {
                    existingStock.setCompanyName(stockDetails.getCompanyName());
                    existingStock.setIndustry(stockDetails.getIndustry());
                    existingStock.setIsActive(stockDetails.getIsActive());

                    return ResponseEntity.ok(stockRepository.save(existingStock));
                })
                .orElse(ResponseEntity.notFound().build());
    }
}
