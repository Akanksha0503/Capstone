import time
from selenium.webdriver.common.by import By


class Keywords:
    def __init__(self, driver):
        self.driver = driver

    # --------------------------
    # Generic Keywords
    # --------------------------
    def navigate_to_url(self, url):
        """Open a given URL."""
        self.driver.get(url)
        return True

    def enter_text(self, by, locator, text):
        """Enter text into any input field."""
        element = self.driver.find_element(by, locator)
        element.clear()
        element.send_keys(text)
        return True

    def click_element(self, by, locator):
        """Click any element."""
        self.driver.find_element(by, locator).click()
        return True

    def verify_page_title(self, expected_title):
        """Verify if page title contains given text."""
        return expected_title.lower() in self.driver.title.lower()

    # --------------------------
    # Application-Specific Keywords (nopCommerce)
    # --------------------------
    def login(self, username, password):
        """Perform login using username and password."""
        self.enter_text(By.ID, "Email", username)
        self.enter_text(By.ID, "Password", password)
        self.click_element(By.XPATH, "//button[normalize-space()='Log in']")
        return True

    def logout(self):
        """Log out from admin."""
        try:
            self.click_element(By.XPATH, "//a[normalize-space()='Logout']")
            return True
        except:
            return False

    def verify_login_successful(self):
        """Verify dashboard is visible after login."""
        time.sleep(2)
        try:
            dashboard = self.driver.find_element(By.XPATH, "//h1[normalize-space()='Dashboard']")
            return dashboard.is_displayed()
        except:
            return False

    def verify_login_failed(self):
        """Verify invalid login error message."""
        try:
            msg = self.driver.find_element(By.CSS_SELECTOR, ".message-error").text
            return "Login was unsuccessful" in msg
        except:
            return False

    # --------------------------
    # Orders Module Keywords
    # --------------------------
    def open_orders_page(self):
        """Navigate to Sales → Orders"""
        self.click_element(By.XPATH, "//p[normalize-space()='Sales']")
        time.sleep(1)
        self.click_element(By.XPATH, "//p[normalize-space()='Orders']")
        time.sleep(2)
        return self.verify_page_title("Orders")

    def search_order_by_id(self, order_id):
        """Search for a specific order by ID"""
        self.enter_text(By.ID, "GoDirectlyToCustomOrderNumber", order_id)
        self.click_element(By.ID, "go-to-order-by-number")
        time.sleep(2)
        return True

    # --------------------------
    # Products Module Keywords
    # --------------------------
    def open_products_page(self):
        """Navigate to Catalog → Products"""
        self.click_element(By.XPATH, "//p[normalize-space()='Catalog']")
        time.sleep(1)
        self.click_element(By.XPATH, "//p[normalize-space()='Products']")
        time.sleep(2)
        return self.verify_page_title("Products")

    def search_product_by_name(self, product_name):
        """Search product by name"""
        self.enter_text(By.ID, "SearchProductName", product_name)
        self.click_element(By.ID, "search-products")
        time.sleep(2)
        products = self.driver.find_elements(By.XPATH, "//table[@id='products-grid']//tbody/tr")
        for p in products:
            if product_name.lower() in p.text.lower():
                return True
        return False
