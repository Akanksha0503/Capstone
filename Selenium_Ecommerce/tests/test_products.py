#pytest Selenium_Ecommerce/tests/test_products.py -v -s -n auto --clean-alluredir --alluredir=Selenium_Ecommerce/Output/reports/report-products/allure-results --html=Selenium_Ecommerce/Output/reports/report-products/products_report.html
#allure generate Selenium_Ecommerce/Output/reports/report-products/allure-results -o  Selenium_Ecommerce/Output/reports/report-products/allure-report --clean
#allure open Selenium_Ecommerce/Output/reports/report-products/allure-report


import pytest
import allure


# Page imports
from Selenium_Ecommerce.pages.LoginPage import LoginPage
from Selenium_Ecommerce.pages.DashboardPage import DashboardPage
from Selenium_Ecommerce.modules.ProductsModule import ProductsModule
from Selenium_Ecommerce.utils.data_loader import load_test_data
from Selenium_Ecommerce.modules.BaseModule import BaseModule





# ------------------------------------------------------------------------
#  Login Fixture
# ------------------------------------------------------------------------
@pytest.fixture
def login_fixture(setup):
    driver = setup
    login_page = LoginPage(driver)
    driver.get("https://admin-demo.nopcommerce.com/login?ReturnUrl=%2Fadmin%2F")
    login_page.login("admin@yourstore.com", "admin")
    dashboard = DashboardPage(driver)
    assert "Dashboard" in dashboard.get_title()
    yield driver, dashboard


# ------------------------------------------------------------------------
# Products Test Suite
# ------------------------------------------------------------------------
@pytest.mark.products
@allure.feature("Products Module")
class TestProductsModule:
    """
    Tests to verify Products page search functionality.
    Screenshots are taken on SUCCESS only.
    """

    @pytest.fixture(autouse=True)
    def setup_products(self, setup):
        """Initialize ProductsPage"""
        self.driver = setup
        self.products_page = ProductsModule(self.driver)
        self.driver.get("https://admin-demo.nopcommerce.com/login?ReturnUrl=%2Fadmin%2F")

        # Login once before navigating to Products (demo admin creds)
        from Selenium_Ecommerce.pages.LoginPage import LoginPage
        login = LoginPage(self.driver)
        login.login("admin@yourstore.com", "admin")

        self.products_page.go_to_products()

    @pytest.mark.parametrize("case", load_test_data("Selenium_Ecommerce/utils/data/product_data.csv"))
    @allure.story("Search Products via File Data (CSV/XLSX/XML)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_product_by_name(self, case):
        """
        Searches for products using data from external files.
        Captures screenshots only if search succeeds.
        """
        product_name = case["product_name"]
        expected = case["expected"]

        with allure.step(f"Searching for product: {product_name}"):
            self.products_page.go_to_products()
            result = self.products_page.search_product_by_name(product_name)

            if result and expected == "Pass":
                self.products_page.take_screenshot("test_products", f"found_{product_name}")
                print(f" Product '{product_name}' found successfully.")
            else:
                assert expected == "Fail", f" Product '{product_name}' not found, but expected Pass."


