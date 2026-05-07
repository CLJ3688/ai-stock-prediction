package com.taiex.api.repository;

import com.taiex.api.model.NewsSentiment;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface NewsSentimentRepository extends JpaRepository<NewsSentiment, Long> {
    List<NewsSentiment> findByStockSymbolOrderByNewsDateDesc(String symbol);
}
