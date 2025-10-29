-- Portfolio Management System Database Schema
-- Created: December 2024 - January 2025

CREATE DATABASE IF NOT EXISTS portfolio_management;
USE portfolio_management;

-- Table 1: Users (Investors/Clients)
CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    date_of_birth DATE,
    address TEXT,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('active', 'inactive', 'suspended') DEFAULT 'active',
    INDEX idx_email (email)
);

-- Table 2: Portfolios
CREATE TABLE Portfolios (
    portfolio_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    portfolio_name VARCHAR(100) NOT NULL,
    portfolio_type ENUM('aggressive', 'moderate', 'conservative') NOT NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_value DECIMAL(15, 2) DEFAULT 0.00,
    currency VARCHAR(3) DEFAULT 'USD',
    status ENUM('active', 'closed') DEFAULT 'active',
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
);

-- Table 3: Asset Categories
CREATE TABLE Asset_Categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    risk_level ENUM('low', 'medium', 'high') NOT NULL
);

-- Table 4: Assets (Stocks, Bonds, etc.)
CREATE TABLE Assets (
    asset_id INT PRIMARY KEY AUTO_INCREMENT,
    category_id INT NOT NULL,
    asset_symbol VARCHAR(10) UNIQUE NOT NULL,
    asset_name VARCHAR(100) NOT NULL,
    asset_type ENUM('stock', 'bond', 'mutual_fund', 'etf', 'commodity', 'crypto') NOT NULL,
    current_price DECIMAL(12, 4) NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    exchange VARCHAR(50),
    FOREIGN KEY (category_id) REFERENCES Asset_Categories(category_id),
    INDEX idx_symbol (asset_symbol)
);

-- Table 5: Portfolio Holdings
CREATE TABLE Portfolio_Holdings (
    holding_id INT PRIMARY KEY AUTO_INCREMENT,
    portfolio_id INT NOT NULL,
    asset_id INT NOT NULL,
    quantity DECIMAL(15, 6) NOT NULL,
    purchase_price DECIMAL(12, 4) NOT NULL,
    purchase_date DATE NOT NULL,
    current_value DECIMAL(15, 2) GENERATED ALWAYS AS (quantity * purchase_price) STORED,
    FOREIGN KEY (portfolio_id) REFERENCES Portfolios(portfolio_id) ON DELETE CASCADE,
    FOREIGN KEY (asset_id) REFERENCES Assets(asset_id),
    INDEX idx_portfolio_asset (portfolio_id, asset_id)
);

-- Table 6: Transactions
CREATE TABLE Transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    portfolio_id INT NOT NULL,
    asset_id INT NOT NULL,
    transaction_type ENUM('buy', 'sell', 'dividend') NOT NULL,
    quantity DECIMAL(15, 6) NOT NULL,
    price_per_unit DECIMAL(12, 4) NOT NULL,
    total_amount DECIMAL(15, 2) GENERATED ALWAYS AS (quantity * price_per_unit) STORED,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fees DECIMAL(10, 2) DEFAULT 0.00,
    notes TEXT,
    FOREIGN KEY (portfolio_id) REFERENCES Portfolios(portfolio_id),
    FOREIGN KEY (asset_id) REFERENCES Assets(asset_id),
    INDEX idx_portfolio_date (portfolio_id, transaction_date)
);

-- Table 7: Performance Metrics
CREATE TABLE Performance_Metrics (
    metric_id INT PRIMARY KEY AUTO_INCREMENT,
    portfolio_id INT NOT NULL,
    metric_date DATE NOT NULL,
    total_value DECIMAL(15, 2) NOT NULL,
    daily_return DECIMAL(8, 4),
    total_return DECIMAL(8, 4),
    benchmark_return DECIMAL(8, 4),
    FOREIGN KEY (portfolio_id) REFERENCES Portfolios(portfolio_id) ON DELETE CASCADE,
    UNIQUE KEY unique_portfolio_date (portfolio_id, metric_date),
    INDEX idx_date (metric_date)
);

-- Table 8: Watchlist
CREATE TABLE Watchlist (
    watchlist_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    asset_id INT NOT NULL,
    added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    target_price DECIMAL(12, 4),
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (asset_id) REFERENCES Assets(asset_id),
    UNIQUE KEY unique_user_asset (user_id, asset_id)
);

-- Sample Data Insertion

-- Insert Asset Categories
INSERT INTO Asset_Categories (category_name, description, risk_level) VALUES
('Technology', 'Technology sector stocks and assets', 'high'),
('Healthcare', 'Healthcare and pharmaceutical companies', 'medium'),
('Finance', 'Banking and financial services', 'medium'),
('Energy', 'Oil, gas, and renewable energy', 'high'),
('Real Estate', 'REITs and property investments', 'low'),
('Government Bonds', 'Treasury and government securities', 'low');

-- Insert Sample Users
INSERT INTO Users (first_name, last_name, email, phone, date_of_birth, address) VALUES
('John', 'Doe', 'john.doe@email.com', '555-0101', '1985-03-15', '123 Main St, New York, NY'),
('Jane', 'Smith', 'jane.smith@email.com', '555-0102', '1990-07-22', '456 Oak Ave, Boston, MA'),
('Robert', 'Johnson', 'robert.j@email.com', '555-0103', '1978-11-30', '789 Pine Rd, Chicago, IL');

-- Insert Sample Assets
INSERT INTO Assets (category_id, asset_symbol, asset_name, asset_type, current_price, exchange) VALUES
(1, 'AAPL', 'Apple Inc.', 'stock', 178.50, 'NASDAQ'),
(1, 'MSFT', 'Microsoft Corporation', 'stock', 425.30, 'NASDAQ'),
(1, 'GOOGL', 'Alphabet Inc.', 'stock', 162.75, 'NASDAQ'),
(2, 'JNJ', 'Johnson & Johnson', 'stock', 155.80, 'NYSE'),
(3, 'JPM', 'JPMorgan Chase', 'stock', 218.45, 'NYSE'),
(4, 'XOM', 'Exxon Mobil', 'stock', 112.30, 'NYSE'),
(5, 'VNQ', 'Vanguard Real Estate ETF', 'etf', 95.60, 'NYSE'),
(6, 'TBond30', 'US 30-Year Treasury', 'bond', 98.75, 'US Treasury');

-- Insert Sample Portfolios
INSERT INTO Portfolios (user_id, portfolio_name, portfolio_type, total_value) VALUES
(1, 'Growth Portfolio', 'aggressive', 150000.00),
(1, 'Retirement Fund', 'conservative', 250000.00),
(2, 'Balanced Investment', 'moderate', 100000.00),
(3, 'Tech Focus', 'aggressive', 75000.00);

-- Insert Sample Portfolio Holdings
INSERT INTO Portfolio_Holdings (portfolio_id, asset_id, quantity, purchase_price, purchase_date) VALUES
(1, 1, 100, 175.20, '2024-01-15'),
(1, 2, 50, 420.50, '2024-02-10'),
(1, 3, 75, 158.30, '2024-03-05'),
(2, 4, 200, 152.40, '2023-06-20'),
(2, 8, 1000, 98.50, '2023-08-15'),
(3, 1, 50, 172.80, '2024-01-20'),
(3, 5, 100, 215.30, '2024-02-15'),
(4, 1, 150, 176.40, '2024-01-10'),
(4, 2, 80, 418.90, '2024-01-25');

-- Insert Sample Transactions
INSERT INTO Transactions (portfolio_id, asset_id, transaction_type, quantity, price_per_unit, fees, notes) VALUES
(1, 1, 'buy', 100, 175.20, 9.99, 'Initial investment in Apple'),
(1, 2, 'buy', 50, 420.50, 12.50, 'Microsoft position'),
(2, 4, 'buy', 200, 152.40, 15.00, 'Healthcare diversification'),
(3, 1, 'buy', 50, 172.80, 8.99, 'Apple shares for balanced portfolio'),
(1, 1, 'dividend', 2.5, 0.96, 0.00, 'Quarterly dividend payment');

-- Useful Queries for Portfolio Management

-- Query 1: View user portfolios with total value
CREATE VIEW v_user_portfolios AS
SELECT 
    u.user_id,
    CONCAT(u.first_name, ' ', u.last_name) AS user_name,
    p.portfolio_id,
    p.portfolio_name,
    p.portfolio_type,
    p.total_value,
    p.status,
    COUNT(ph.holding_id) AS total_holdings
FROM Users u
JOIN Portfolios p ON u.user_id = p.user_id
LEFT JOIN Portfolio_Holdings ph ON p.portfolio_id = ph.portfolio_id
GROUP BY u.user_id, p.portfolio_id;

-- Query 2: Portfolio performance summary
CREATE VIEW v_portfolio_performance AS
SELECT 
    p.portfolio_id,
    p.portfolio_name,
    SUM(ph.quantity * a.current_price) AS current_market_value,
    SUM(ph.current_value) AS cost_basis,
    SUM(ph.quantity * a.current_price) - SUM(ph.current_value) AS unrealized_gain_loss,
    ROUND(((SUM(ph.quantity * a.current_price) - SUM(ph.current_value)) / SUM(ph.current_value) * 100), 2) AS return_percentage
FROM Portfolios p
JOIN Portfolio_Holdings ph ON p.portfolio_id = ph.portfolio_id
JOIN Assets a ON ph.asset_id = a.asset_id
GROUP BY p.portfolio_id;

-- Query 3: Top performing assets
SELECT 
    a.asset_symbol,
    a.asset_name,
    a.asset_type,
    a.current_price,
    COUNT(ph.holding_id) AS held_by_portfolios,
    SUM(ph.quantity) AS total_quantity_held
FROM Assets a
LEFT JOIN Portfolio_Holdings ph ON a.asset_id = ph.asset_id
GROUP BY a.asset_id
ORDER BY held_by_portfolios DESC, total_quantity_held DESC
LIMIT 10;

-- Stored Procedure: Add transaction and update holdings
DELIMITER //
CREATE PROCEDURE sp_add_transaction(
    IN p_portfolio_id INT,
    IN p_asset_id INT,
    IN p_transaction_type ENUM('buy', 'sell', 'dividend'),
    IN p_quantity DECIMAL(15,6),
    IN p_price DECIMAL(12,4),
    IN p_fees DECIMAL(10,2),
    IN p_notes TEXT
)
BEGIN
    DECLARE existing_quantity DECIMAL(15,6);
    
    -- Insert transaction
    INSERT INTO Transactions (portfolio_id, asset_id, transaction_type, quantity, price_per_unit, fees, notes)
    VALUES (p_portfolio_id, p_asset_id, p_transaction_type, p_quantity, p_price, p_fees, p_notes);
    
    -- Update holdings based on transaction type
    IF p_transaction_type = 'buy' THEN
        -- Check if holding exists
        SELECT quantity INTO existing_quantity 
        FROM Portfolio_Holdings 
        WHERE portfolio_id = p_portfolio_id AND asset_id = p_asset_id;
        
        IF existing_quantity IS NULL THEN
            -- Create new holding
            INSERT INTO Portfolio_Holdings (portfolio_id, asset_id, quantity, purchase_price, purchase_date)
            VALUES (p_portfolio_id, p_asset_id, p_quantity, p_price, CURDATE());
        ELSE
            -- Update existing holding
            UPDATE Portfolio_Holdings
            SET quantity = quantity + p_quantity,
                purchase_price = ((quantity * purchase_price) + (p_quantity * p_price)) / (quantity + p_quantity)
            WHERE portfolio_id = p_portfolio_id AND asset_id = p_asset_id;
        END IF;
    ELSEIF p_transaction_type = 'sell' THEN
        UPDATE Portfolio_Holdings
        SET quantity = quantity - p_quantity
        WHERE portfolio_id = p_portfolio_id AND asset_id = p_asset_id;
        
        -- Remove holding if quantity is 0
        DELETE FROM Portfolio_Holdings
        WHERE portfolio_id = p_portfolio_id AND asset_id = p_asset_id AND quantity <= 0;
    END IF;
END //
DELIMITER ;
