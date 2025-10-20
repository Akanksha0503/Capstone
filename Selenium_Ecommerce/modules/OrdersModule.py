import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Selenium_Ecommerce.modules.BaseModule import BaseModule


class OrdersModule(BaseModule):
    # -------------------- Locators --------------------
    order_id_input = (By.ID, "GoDirectlyToCustomOrderNumber")
    go_button = (By.XPATH, "//button[contains(.,'Go')]")
    order_status_div = (By.CSS_SELECTOR, "div.input-group-text.align-items-start > div.font-weight-bold")


    sales_menu = (By.XPATH, "//p[normalize-space()='Sales']")
    orders_submenu = (By.XPATH, "//p[normalize-space()='Orders']")


    billing_email_input = (By.ID, "BillingEmail")
    billing_lastname_input = (By.ID, "BillingLastName")
    search_button = (By.ID, "search-orders")


    status_cell = (By.XPATH, "//table[@id='orders-grid']//tbody/tr[1]/td[3]")

    # Locator for orders table result
    order_row = (By.XPATH, "//table//tr[td]")

    @allure.step("Navigating to Orders Page")
    def go_to_orders(self):
        """Navigate from Dashboard → Sales → Orders (Firefox-safe)."""
        print(" Navigating to Orders section...")

        try:
            sales_menu = (By.XPATH, "//p[normalize-space()='Sales']")
            orders_menu = (By.XPATH, "//p[normalize-space()='Orders']")

            # Step 1: Scroll and click 'Sales'
            self.scroll_to_element(*sales_menu)
            print("  Scrolled to Sales menu")

            try:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(sales_menu)
                ).click()
            except Exception:
                print(" Normal click failed — using JS click for Sales menu")
                element = self.driver.find_element(*sales_menu)
                self.driver.execute_script("arguments[0].click();", element)

            time.sleep(1)

            # Step 2: Scroll and click 'Orders'
            self.scroll_to_element(*orders_menu)
            print("  Scrolled to Orders submenu")

            try:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(orders_menu)
                ).click()
            except Exception:
                print(" Normal click failed — using JS click for Orders submenu")
                element = self.driver.find_element(*orders_menu)
                self.driver.execute_script("arguments[0].click();", element)

            # Step 3: Wait until Orders page loads
            WebDriverWait(self.driver, 15).until(EC.title_contains("Orders"))
            print(" Orders page loaded successfully!")
            self.take_screenshot("test_orders", "orders_page_loaded")

        except Exception as e:
            print(f" Orders navigation failed: {e}")
            raise

    def verify_order_status(self, order_id):
        """Enter Order ID, click Go, and verify order status (Pending/Processing/Complete)."""
        print(f" Verifying status for Order ID: {order_id}")
        try:
            # Step 1: Type order ID
            self.clear_and_type(By.ID, "GoDirectlyToCustomOrderNumber", order_id)

            # Step 2: Locate the 'Go' button
            go_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Go']"))
            )

            # Step 3: Try normal click first
            try:
                go_button.click()
                print(" Clicked 'Go' button (normal click)")
            except Exception:
                # Firefox fallback: use JS click if normal click fails
                self.driver.execute_script("arguments[0].click();", go_button)
                print("Clicked 'Go' button via JavaScript (Firefox fallback)")

            # Step 4: Wait for status box to appear (Processing / Pending / Complete)
            status_locator = (By.XPATH, "//div[@class='font-weight-bold']")
            WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(status_locator))
            status = self.driver.find_element(*status_locator).text.strip()

            print(f" Order ID {order_id} status: {status}")
            self.take_screenshot("test_orders", f"order_status_{order_id}_{status.lower()}")
            return status

        except Exception as e:
            print(f" Timeout or failure while verifying order ID {order_id}: {e}")
            return None

        # -------------------- Search by Email --------------------

    def search_by_email(self, email):
        """Search orders by Billing Email."""
        print(f" Searching orders by email: {email}")
        try:
            self.clear_and_type(*self.billing_email_input, email)
            self.click_element(*self.search_button)
            time.sleep(2)

            # Wait for table rows to load
            rows = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(self.order_row)
            )
            for row in rows:
                if email.lower() in row.text.lower():
                    print(f" Found order with email: {email}")
                    self.take_screenshot("test_orders", f"search_email_success_{email.replace('@', '_')}")
                    return True
            print(f" No matching order found for email: {email}")
            return False

        except Exception as e:
            print(f" Error while searching by email {email}: {e}")
            return False

    def search_by_last_name(self, last_name):
        """Search orders by Billing Last Name."""
        print(f" Searching orders by last name: {last_name}")
        try:
            self.clear_and_type(*self.billing_lastname_input, last_name)
            self.click_element(*self.search_button)
            time.sleep(2)

            # Wait for table rows to load
            rows = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(self.order_row)
            )
            for row in rows:
                if last_name.lower() in row.text.lower():
                    print(f" Found order with last name: {last_name}")
                    self.take_screenshot("test_orders", f"search_lastname_success_{last_name}")
                    return True
            print(f" No matching order found for last name: {last_name}")
            return False

        except Exception as e:
            print(f" Error while searching by last name {last_name}: {e}")
            return False