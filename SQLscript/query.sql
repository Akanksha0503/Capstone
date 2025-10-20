-- ================================================================
-- BANKING DATABASE OPERATIONS
-- ================================================================
-- This script demonstrates basic SQL operations on the banking database:
-- - Basic Queries: SELECT, UPDATE, DELETE
-- - JOIN Query: Customers + Transactions (as "Orders" table)
-- - CREATE VIEW: Active Customers (customers with transactions in last year)
-- - Additional Queries: Aggregates, Subqueries, Indexes, Stored Procedures (SQLite-compatible)
--
-- Assumptions:
-- - Database: SQLite (adaptable to MySQL/PostgreSQL)
-- - Tables: branches, customers, transactions (from create.sql and insert.sql)
-- - Current Date: October 11, 2025 (for active customers: transactions since 2024-10-11)
-- ================================================================
 USE banking;
-- ================================================================
-- 1. BASIC QUERIES (SELECT, UPDATE, DELETE)
-- ================================================================

-- a. SELECT: Retrieve all customers (first 5 for brevity)
SELECT * FROM customers LIMIT 5;

-- b. SELECT with WHERE: Customers with balance > 50000 (first 5)
SELECT name, city, account_balance
FROM customers
WHERE account_balance > 50000
ORDER BY account_balance DESC
LIMIT 5;

-- c. SELECT with LIKE: Customers whose name starts with 'A' (case-insensitive)
SELECT name, city
FROM customers
WHERE UPPER(name) LIKE 'A%';

-- d. UPDATE: Increase balance by 10% for all Savings accounts
UPDATE customers
SET account_balance = account_balance * 1.10
WHERE LOWER(account_type) = 'savings';

-- Verify UPDATE:
SELECT name, account_balance
FROM customers
WHERE LOWER(account_type) = 'savings'
LIMIT 3;

-- e. DELETE: Remove customers with balance < 1000 (inactive/low-balance)
DELETE FROM customers
WHERE account_balance < 10000;

-- Verify DELETE (count remaining customers):
SELECT COUNT(*) AS remaining_customers FROM customers;

-- ================================================================
-- 2. JOIN QUERY (Customer + Transactions as "Orders" Table)
-- ================================================================

-- Basic INNER JOIN: Customer details with their transactions (last 5 by date)
SELECT c.name, c.city, c.account_type, t.transaction_date, t.amount, t.transaction_type, t.channel
FROM customers c
INNER JOIN transactions t ON c.customer_id = t.customer_id
ORDER BY t.transaction_date DESC
LIMIT 5;

-- LEFT JOIN: All customers with their total transaction amount (0 if no transactions)
SELECT c.name, c.customer_id,
       COALESCE(SUM(t.amount), 0) AS total_transaction_amount,
       COUNT(t.transaction_id) AS transaction_count
FROM customers c
LEFT JOIN transactions t ON c.customer_id = t.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_transaction_amount DESC
LIMIT 10;

-- CROSS JOIN Example (for demo: All customers x All branches - use sparingly!)
SELECT c.name, b.branch_name
FROM customers c
CROSS JOIN branches b
LIMIT 5;  -- Just 5 for brevity

-- ================================================================
-- CREATE A VIEW
-- ================================================================

-- Drop existing view if it exists
DROP VIEW IF EXISTS active_customers;

-- Create updatable view (single table, no aggregates/JOINs in FROM)
CREATE VIEW active_customers AS
SELECT c.customer_id, c.name, c.gender, c.date_of_birth, c.city, c.state,
       c.phone_number, c.email, c.branch_code, c.account_type, c.account_balance
FROM customers c
WHERE EXISTS (
    SELECT 1 FROM transactions t
    WHERE t.customer_id = c.customer_id
    AND t.transaction_date >= '2024-10-11'  -- Last year from Oct 11, 2025
);

-- ================================================================
-- TEST THE VIEW
-- ================================================================

-- Query the view (first 5 active customers)
SELECT * FROM active_customers LIMIT 5;

-- UPDATE via view (updates underlying customers table)
UPDATE active_customers
SET city = 'Updated Mumbai', account_balance = account_balance + 1000
WHERE customer_id = 1;  -- Replace 1 with a valid active customer_id

-- Verify UPDATE
SELECT * FROM active_customers WHERE customer_id = 1;

-- DELETE via view (deletes from customers, cascades to transactions if FK set)
DELETE FROM active_customers WHERE customer_id = 1;

-- Verify DELETE
SELECT COUNT(*) AS active_count FROM active_customers;

-- ================================================================
-- END OF SCRIPT
-- ================================================================
-- ================================================================
-- 4. ADDITIONAL QUERIES (Aggregates, Subqueries, Indexes, etc.)
-- ================================================================

-- a. Aggregate: Total balance by account type
SELECT LOWER(account_type) AS account_type,
       COUNT(*) AS customer_count,
       SUM(account_balance) AS total_balance,
       AVG(account_balance) AS avg_balance
FROM customers
GROUP BY LOWER(account_type)
ORDER BY total_balance DESC;

-- b. Subquery: Customers with above-average balance
SELECT name, account_balance
FROM customers
WHERE account_balance > (SELECT AVG(account_balance) FROM customers)
ORDER BY account_balance DESC
LIMIT 5;

-- c. EXISTS Subquery: Customers who have transactions (using EXISTS)
SELECT name, city
FROM customers c
WHERE EXISTS (
    SELECT 1 FROM transactions t WHERE t.customer_id = c.customer_id
)
LIMIT 5;

-- d. UNION: Combine Savings and Current account customers
SELECT name, account_type FROM customers WHERE LOWER(account_type) = 'savings'
UNION
SELECT name, account_type FROM customers WHERE LOWER(account_type) = 'current'
ORDER BY name
LIMIT 10;

-- e. CASE Statement: Categorize balances
SELECT name, account_balance,
       CASE
           WHEN account_balance > 100000 THEN 'High'
           WHEN account_balance > 50000 THEN 'Medium'
           ELSE 'Low'
       END AS balance_category
FROM customers
ORDER BY account_balance DESC
LIMIT 5;

-- f. Window Function: Rank customers by balance within each branch
SELECT name, branch_code, account_balance,
       RANK() OVER (PARTITION BY branch_code ORDER BY account_balance DESC) AS rank_in_branch
FROM customers
LIMIT 10;

-- g. CREATE INDEX: For performance on name searches
CREATE INDEX idx_customer_name ON customers(name);
CREATE INDEX idx_transaction_date ON transactions(transaction_date);

-- ================================================================
-- END OF SCRIPT
