-- ================================================================
-- FINAL CORRECTED STORED PROCEDURES FOR BANKING DATABASE
-- ================================================================
-- Key Fixes:
-- - CHECK Constraint: All 'channel' values set to 'ONLINE' (valid: MOBILE, ONLINE, BRANCH, ATM).
-- - Transaction Type/Category: Ensured 'CREDIT'/'DEBIT' and 'adjustment'/'transfer' (valid categories).
-- - Syntax: Fixed regex (no extra space), LEAVE labels, default params handled inside.
-- - Validation: Added ABS for amount in logs to ensure positive values.
-- - Tested: Procedures compile and run without violations.
--
-- Run: mysql -u root -p banking < final_corrected_procedures.sql
-- ================================================================

USE banking;

-- ================================================================
-- 1. STORED PROCEDURE: Add New Customer
-- ================================================================
-- No transaction insert here, so no CHECK violation.

DELIMITER //
DROP PROCEDURE IF EXISTS AddNewCustomer //
CREATE PROCEDURE AddNewCustomer(
    IN p_name VARCHAR(100),
    IN p_gender VARCHAR(10),
    IN p_date_of_birth DATE,
    IN p_city VARCHAR(100),
    IN p_state VARCHAR(100),
    IN p_phone_number VARCHAR(15),
    IN p_email VARCHAR(100),
    IN p_branch_code VARCHAR(10),
    IN p_account_type VARCHAR(50),
    IN p_account_balance DECIMAL(10,2),
    OUT p_customer_id INT,
    OUT p_message VARCHAR(255)
)
proc_label: BEGIN
    DECLARE v_age INT;
    DECLARE v_current_year INT DEFAULT YEAR(CURDATE());
    DECLARE v_days_in_month INT;

    SET p_customer_id = NULL;
    SET p_message = '';

    IF p_name RLIKE '^[A-Za-z\\s\'-]+$' = 0 OR LENGTH(TRIM(p_name)) = 0 THEN
        SET p_message = CONCAT('Error: Name "', p_name, '" must be alphabetic with spaces/hyphens/apostrophes only.');
        LEAVE proc_label;
    END IF;

    IF UPPER(p_gender) NOT IN ('M', 'F') THEN
        SET p_message = CONCAT('Error: Gender "', p_gender, '" must be M or F.');
        LEAVE proc_label;
    END IF;

    IF YEAR(p_date_of_birth) >= v_current_year OR MONTH(p_date_of_birth) NOT BETWEEN 1 AND 12 THEN
        SET p_message = CONCAT('Error: DOB "', p_date_of_birth, '" year must be < ', v_current_year, ', month 1-12.');
        LEAVE proc_label;
    END IF;

    SET v_days_in_month = DAY(LAST_DAY(STR_TO_DATE(CONCAT(YEAR(p_date_of_birth), '-', MONTH(p_date_of_birth), '-01'), '%Y-%m-%d')));
    IF DAY(p_date_of_birth) > v_days_in_month OR DAY(p_date_of_birth) < 1 THEN
        SET p_message = CONCAT('Error: Invalid day ', DAY(p_date_of_birth), ' for month ', MONTH(p_date_of_birth), ' (max ', v_days_in_month, ').');
        LEAVE proc_label;
    END IF;

    SET v_age = v_current_year - YEAR(p_date_of_birth) -
                IF((MONTH(CURDATE()) < MONTH(p_date_of_birth) OR
                    (MONTH(CURDATE()) = MONTH(p_date_of_birth) AND DAY(CURDATE()) < DAY(p_date_of_birth))), 1, 0);
    IF v_age <= 18 THEN
        SET p_message = CONCAT('Error: Age must be > 18. Calculated age for "', p_date_of_birth, '": ', v_age);
        LEAVE proc_label;
    END IF;

    IF p_city RLIKE '^[A-Za-z\\s]+$' = 0 OR LENGTH(TRIM(p_city)) = 0 THEN
        SET p_message = CONCAT('Error: City "', p_city, '" must be alphabetic with spaces only.');
        LEAVE proc_label;
    END IF;

    IF p_state RLIKE '^[A-Za-z\\s]+$' = 0 OR LENGTH(TRIM(p_state)) = 0 THEN
        SET p_message = CONCAT('Error: State "', p_state, '" must be alphabetic with spaces only.');
        LEAVE proc_label;
    END IF;

    IF p_phone_number RLIKE '^[0-9]{10}$' = 0 THEN
        SET p_message = CONCAT('Error: Phone "', p_phone_number, '" must be exactly 10 digits.');
        LEAVE proc_label;
    END IF;

    IF p_email RLIKE '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$' = 0 THEN
        SET p_message = CONCAT('Error: Invalid email format "', p_email, '".');
        LEAVE proc_label;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM branches WHERE branch_code = p_branch_code) THEN
        SET p_message = CONCAT('Error: Branch code "', p_branch_code, '" does not exist.');
        LEAVE proc_label;
    END IF;

    IF UPPER(p_account_type) NOT IN ('SAVINGS', 'CURRENT', 'FIXED DEPOSIT') THEN
        SET p_message = CONCAT('Error: Account type "', p_account_type, '" must be Savings, Current, or Fixed Deposit.');
        LEAVE proc_label;
    END IF;

    IF p_account_balance < 0 THEN
        SET p_message = CONCAT('Error: Balance "', p_account_balance, '" must be >= 0.');
        LEAVE proc_label;
    END IF;

    INSERT INTO customers (name, gender, date_of_birth, city, state, phone_number, email, branch_code, account_type, account_balance)
    VALUES (p_name, p_gender, p_date_of_birth, p_city, p_state, p_phone_number, p_email, p_branch_code, p_account_type, p_account_balance);

    SET p_customer_id = LAST_INSERT_ID();
    SET p_message = CONCAT(' Customer added successfully. ID: ', p_customer_id, ', Age: ', v_age);
END proc_label //
DELIMITER ;

-- ================================================================
-- 2. STORED PROCEDURE: Update Customer Balance (Fixed CHECK)
-- ================================================================

DELIMITER //
DROP PROCEDURE IF EXISTS UpdateCustomerBalance //
CREATE PROCEDURE UpdateCustomerBalance(
    IN p_customer_id INT,
    IN p_new_balance DECIMAL(10,2),
    OUT p_message VARCHAR(255)
)
proc_label: BEGIN
    DECLARE v_current_balance DECIMAL(10,2);
    DECLARE v_diff DECIMAL(10,2);
    DECLARE v_branch_code VARCHAR(10);

    SET p_message = '';

    SELECT account_balance, branch_code INTO v_current_balance, v_branch_code
    FROM customers WHERE customer_id = p_customer_id;

    IF v_current_balance IS NULL THEN
        SET p_message = 'Error: Customer not found.';
        LEAVE proc_label;
    END IF;

    IF p_new_balance < 0 THEN
        SET p_message = 'Error: Balance cannot be negative.';
        LEAVE proc_label;
    END IF;

    SET v_diff = p_new_balance - v_current_balance;

    UPDATE customers SET account_balance = p_new_balance WHERE customer_id = p_customer_id;

    IF v_diff != 0 THEN
        INSERT INTO transactions (customer_id, branch_code, amount, transaction_type, transaction_category, transaction_date, channel)
        VALUES (p_customer_id, v_branch_code, ABS(v_diff),
                CASE WHEN v_diff > 0 THEN 'CREDIT' ELSE 'DEBIT' END,
                'adjustment', CURDATE(), 'ONLINE');  -- Valid channel: ONLINE
    END IF;

    SET p_message = CONCAT(' Balance updated to ', p_new_balance, '. Difference: ', v_diff);
END proc_label //
DELIMITER ;

-- ================================================================
-- 3. STORED PROCEDURE: Delete Customer (No Transaction Insert)
-- ================================================================

DELIMITER //
DROP PROCEDURE IF EXISTS DeleteCustomer //
CREATE PROCEDURE DeleteCustomer(
    IN p_customer_id INT,
    OUT p_message VARCHAR(255)
)
proc_label: BEGIN
    DECLARE v_transaction_count INT DEFAULT 0;

    SET p_message = '';

    IF NOT EXISTS (SELECT 1 FROM customers WHERE customer_id = p_customer_id) THEN
        SET p_message = 'Error: Customer not found.';
        LEAVE proc_label;
    END IF;

    SELECT COUNT(*) INTO v_transaction_count
    FROM transactions t
    WHERE t.customer_id = p_customer_id
    AND t.transaction_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR);

    IF v_transaction_count > 0 THEN
        SET p_message = CONCAT('Error: Customer has ', v_transaction_count, ' recent transactions. Cannot delete.');
        LEAVE proc_label;
    END IF;

    DELETE FROM customers WHERE customer_id = p_customer_id;

    SET p_message = ' Customer deleted successfully.';
END proc_label //
DELIMITER ;

-- ================================================================
-- 4. STORED PROCEDURE: Get Active Customers (No Insert, No CHECK Issue)
-- ================================================================

DELIMITER //
DROP PROCEDURE IF EXISTS GetActiveCustomers //
CREATE PROCEDURE GetActiveCustomers(
    IN p_limit INT,
    OUT p_total_active INT
)
proc_label: BEGIN
    IF p_limit IS NULL OR p_limit < 1 THEN
        SET p_limit = 10;
    END IF;

    SELECT COUNT(DISTINCT c.customer_id) INTO p_total_active
    FROM customers c
    WHERE EXISTS (
        SELECT 1 FROM transactions t
        WHERE t.customer_id = c.customer_id
        AND t.transaction_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
    );

    SELECT c.customer_id, c.name, c.city, c.account_type, c.account_balance,
           COUNT(t.transaction_id) AS transaction_count,
           SUM(CASE WHEN t.transaction_type = 'CREDIT' THEN t.amount ELSE 0 END) AS total_credits,
           SUM(CASE WHEN t.transaction_type = 'DEBIT' THEN t.amount ELSE 0 END) AS total_debits
    FROM customers c
    LEFT JOIN transactions t ON c.customer_id = t.customer_id
    AND t.transaction_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
    WHERE EXISTS (
        SELECT 1 FROM transactions t2
        WHERE t2.customer_id = c.customer_id
        AND t2.transaction_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
    )
    GROUP BY c.customer_id, c.name, c.city, c.account_type, c.account_balance
    ORDER BY c.name ASC
    LIMIT p_limit;
END proc_label //
DELIMITER ;

-- ================================================================
-- 5. STORED PROCEDURE: Transfer Funds (Fixed CHECK - Valid Values)
-- ================================================================

DELIMITER //
DROP PROCEDURE IF EXISTS TransferFunds //
CREATE PROCEDURE TransferFunds(
    IN p_from_customer_id INT,
    IN p_to_customer_id INT,
    IN p_amount DECIMAL(10,2),
    OUT p_message VARCHAR(255)
)
proc_label: BEGIN
    DECLARE v_from_balance DECIMAL(10,2);
    DECLARE v_to_balance DECIMAL(10,2);
    DECLARE v_from_branch VARCHAR(10);
    DECLARE v_to_branch VARCHAR(10);

    SET p_message = '';

    SELECT account_balance, branch_code INTO v_from_balance, v_from_branch
    FROM customers WHERE customer_id = p_from_customer_id;

    IF v_from_balance IS NULL THEN
        SET p_message = 'Error: From customer not found.';
        LEAVE proc_label;
    END IF;

    SELECT account_balance, branch_code INTO v_to_balance, v_to_branch
    FROM customers WHERE customer_id = p_to_customer_id;

    IF v_to_balance IS NULL THEN
        SET p_message = 'Error: To customer not found.';
        LEAVE proc_label;
    END IF;

    IF p_amount <= 0 THEN
        SET p_message = 'Error: Amount must be positive.';
        LEAVE proc_label;
    END IF;

    IF p_amount > v_from_balance THEN
        SET p_message = 'Error: Insufficient funds.';
        LEAVE proc_label;
    END IF;

    START TRANSACTION;

    UPDATE customers SET account_balance = account_balance - p_amount WHERE customer_id = p_from_customer_id;
    UPDATE customers SET account_balance = account_balance + p_amount WHERE customer_id = p_to_customer_id;

    -- Log with valid CHECK values
    INSERT INTO transactions (customer_id, branch_code, amount, transaction_type, transaction_category, transaction_date, channel)
    VALUES
    (p_from_customer_id, v_from_branch, p_amount, 'DEBIT', 'transfer', CURDATE(), 'ONLINE'),  -- Valid: DEBIT, transfer, ONLINE
    (p_to_customer_id, v_to_branch, p_amount, 'CREDIT', 'transfer', CURDATE(), 'ONLINE');     -- Valid: CREDIT, transfer, ONLINE

    COMMIT;

    SET p_message = CONCAT(' Transferred ', p_amount, ' from customer ', p_from_customer_id, ' to ', p_to_customer_id, '.');
END proc_label //
DELIMITER ;

-- ================================================================
-- TEST ALL PROCEDURES (Safe Tests)
-- ================================================================

-- Test AddNewCustomer (valid input)
CALL AddNewCustomer('Rajiv Mehta', 'M', '1990-01-01', 'New York', 'NY', '1234567890', 'john@example.com', 'BR001', 'Savings', 1000.00, @new_id, @msg);
SELECT @new_id AS customer_id, @msg AS message;

-- Test UpdateCustomerBalance (no violation)
CALL UpdateCustomerBalance(1, 110000.00, @msg);
SELECT @msg AS message;

-- Test DeleteCustomer (ID with no recent tx)
CALL DeleteCustomer(50, @msg);
SELECT @msg AS message;

-- Test GetActiveCustomers
CALL GetActiveCustomers(5, @total);
SELECT @total AS total_active_customers;

-- Test TransferFunds (valid amount, no violation)
CALL TransferFunds(1, 2, 500.00, @msg);
SELECT @msg AS message;

-- ================================================================
-- END OF FINAL FIXED SCRIPT
-- ================================================================
