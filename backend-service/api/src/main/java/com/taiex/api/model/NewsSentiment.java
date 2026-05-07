package com.taiex.api.model;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.*;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDate;

@Data
@Entity
@Table(name = "news_sentiment")
public class NewsSentiment {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "symbol", referencedColumnName = "symbol", nullable = false)
    @JsonIgnore
    private Stock stock;

    @Column(name = "news_date", nullable = false)
    private LocalDate newsDate;

    @Column(name = "title", length = 255, nullable = false)
    private String title;

    @Column(name = "sentiment_score", precision = 5, scale = 4, nullable = false)
    private BigDecimal sentimentScore;

    @Column(name = "source_url", columnDefinition = "TEXT")
    private String sourceUrl;
}
