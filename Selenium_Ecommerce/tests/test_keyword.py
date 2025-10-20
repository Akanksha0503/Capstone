import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from Selenium_Ecommerce.pages.Keyword import Keywords
from Selenium_Ecommerce.utils.config import Config


class TestKeywords:

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up Chrome browser for each test."""
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.kw = Keywords(self.driver)
        yield
        self.driver.quit()

    def test_valid_admin_login(self):
        """Verify admin can log in successfully."""
        self.kw.navigate_to_url(Config.BASE_URL)
        self.kw.login(Config.ADMIN_USERNAME, Config.ADMIN_PASSWORD)
        assert self.kw.verify_login_successful() is True

    def test_invalid_login(self):
        """Verify invalid login shows error message."""
        self.kw.navigate_to_url(Config.BASE_URL)
        self.kw.login("wrong_user@store.com", "badpass")
        assert self.kw.verify_login_failed() is True

    def test_open_orders_module(self):
        """Verify navigation to Orders page."""
        self.kw.navigate_to_url(Config.BASE_URL)
        self.kw.login(Config.ADMIN_USERNAME, Config.ADMIN_PASSWORD)
        assert self.kw.open_orders_page() is True

    def test_search_product(self):
        """Verify searching for a product."""
        self.kw.navigate_to_url(Config.BASE_URL)
        self.kw.login(Config.ADMIN_USERNAME, Config.ADMIN_PASSWORD)
        self.kw.open_products_page()
        assert self.kw.search_product_by_name("Build your own computer") is True
