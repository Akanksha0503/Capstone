import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, ElementNotInteractableException
from Selenium_Ecommerce.modules.BaseModule import BaseModule


class ProductsModule(BaseModule):
    # ---------------- Locators ----------------
    CATALOG_MENU = (By.XPATH, "//p[normalize-space()='Catalog']")
    PRODUCTS_SUBMENU = (By.XPATH, "//p[normalize-space()='Products']")
    SEARCH_INPUT = (By.ID, "SearchProductName")
    SEARCH_BUTTON = (By.ID, "search-products")
    PRODUCT_ROW = (By.XPATH, "//table[@id='products-grid']//tbody/tr")

    @allure.step("Navigating to Products Page")
    def go_to_products(self):
        """Navigate from Dashboard → Catalog → Products (cross-browser safe)."""
        print(" Navigating to Products section...")

        try:
            # Step 1: Scroll to Catalog menu
            self.scroll_to_element(*self.CATALOG_MENU)
            print("  Scrolled to Catalog menu")

            # Step 2: Try normal click, fallback to JS
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(self.CATALOG_MENU)
                ).click()
            except (TimeoutException, ElementClickInterceptedException, ElementNotInteractableException):
                print("  Normal click failed — using JS click for Catalog menu")
                element = self.driver.find_element(*self.CATALOG_MENU)
                self.driver.execute_script("arguments[0].click();", element)

            time.sleep(1)

            # Step 3: Scroll to Products submenu
            self.scroll_to_element(*self.PRODUCTS_SUBMENU)
            print("  Scrolled to Products submenu")

            # Step 4: Click Products submenu
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(self.PRODUCTS_SUBMENU)
                ).click()
            except (TimeoutException, ElementClickInterceptedException, ElementNotInteractableException):
                print("  Normal click failed — using JS click for Products submenu")
                element = self.driver.find_element(*self.PRODUCTS_SUBMENU)
                self.driver.execute_script("arguments[0].click();", element)

            # Step 5: Wait for Products page load
            WebDriverWait(self.driver, 15).until(EC.title_contains("Products"))
            print("  Products page loaded successfully!")
            self.take_screenshot("test_products", "products_page_loaded")

        except Exception as e:
            print(f" Products navigation failed: {e}")
            raise

    @allure.step("Searching for a product by name")
    def search_product_by_name(self, product_name):
        """Search for a product by its name and validate result presence."""
        print(f" Searching for product: {product_name}")
        try:
            self.clear_and_type(*self.SEARCH_INPUT, product_name)
            self.click_element(*self.SEARCH_BUTTON)
            time.sleep(2)

            rows = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(self.PRODUCT_ROW)
            )

            for row in rows:
                if product_name.lower() in row.text.lower():
                    print(f"  Product '{product_name}' found in results!")
                    self.take_screenshot("test_products", f"search_success_{product_name}")
                    return True

            print(f"  Product '{product_name}' not found in results.")
            return False

        except Exception as e:
            print(f" Error while searching for product '{product_name}': {e}")
            return False
