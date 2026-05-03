package com.taiex.api.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Data;

@Data
@Entity
@Table(name = "stocks")
public class Stock {

    @Id
    @Column(name = "symbol", length = 10, nullable = false)
    private String symbol;

    @Column(name = "company_name", length = 255, nullable = false)
    private String companyName;

    @Column(name = "industry", length = 255)
    private String industry;

    @Column(name = "is_active", nullable = false)
    private Boolean isActive = true;
}
