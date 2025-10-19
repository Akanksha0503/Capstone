

-- ================================================================
-- Banking Database Schema
-- ================================================================
-- Changes from original:
-- 1. Reordered table creation: branches first (no dependencies), then customers, then transactions.
-- 2. Added FOREIGN KEY to customers(branch_code) REFERENCES branches(branch_code) ON DELETE CASCADE.
-- 3. For transactions: Added ON DELETE CASCADE to both foreign keys to prevent constraint errors on DELETE/UPDATE.
-- 4. Ensured MySQL compatibility (e.g., ENGINE=InnoDB for FK support).
-- 5. Retained CHECK constraints (MySQL 8.0+ supports them).
-- ================================================================

-- Create database (if not exists)
DROP DATABASE IF EXISTS banking;
CREATE DATABASE IF NOT EXISTS banking;
USE banking;

-- Table 1: Branches (no dependencies)
CREATE TABLE IF NOT EXISTS branches (
    branch_code VARCHAR(10) PRIMARY KEY,
    branch_name VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(100),
    ifsc_code VARCHAR(20) UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table 2: Customers (references branches)
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    date_of_birth DATE NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    email VARCHAR(100) NOT NULL,
    branch_code VARCHAR(10) NOT NULL,
    account_type VARCHAR(50) NOT NULL,
    account_balance DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    FOREIGN KEY (branch_code) REFERENCES branches(branch_code) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table 3: Transactions (references customers and branches)
CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    branch_code VARCHAR(10) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    transaction_type VARCHAR(10) NOT NULL CHECK (transaction_type IN ('CREDIT', 'DEBIT')),
    transaction_category VARCHAR(20) NOT NULL CHECK (transaction_category IN ('deposit', 'withdrawal', 'transfer', 'payment', 'adjustment')),  -- Added 'adjustment'
    transaction_date DATE NOT NULL,
    channel VARCHAR(20) NOT NULL CHECK (channel IN ('MOBILE', 'ONLINE', 'BRANCH', 'ATM')),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (branch_code) REFERENCES branches(branch_code) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ================================================================
-- END OF UPDATED CREATE.SQL
-- ================================================================
-- To use: mysql -u root -p < updated_create.sql
-- Then run insert.sql for data.
-- Test DELETE: DELETE FROM customers WHERE customer_id = 50;  -- Now succeeds, auto-deletes transactions.