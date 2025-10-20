

# pytest Selenium_Ecommerce/tests/test_orders.py -v -s --clean-alluredir --alluredir=Selenium_Ecommerce/Output/reports/report-order/allure-results --html=Selenium_Ecommerce/Output/reports/report-order/order_report.html
# allure generate Selenium_Ecommerce/Output/reports/report-order/allure-results -o  Selenium_Ecommerce/Output/reports/report-order/allure-report --clean
 # allure open Selenium_Ecommerce/Output/reports/report-order/allure-report


from Selenium_Ecommerce.modules.OrdersModule import OrdersModule

import pytest
import allure
from Selenium_Ecommerce.pages.LoginPage import LoginPage
from Selenium_Ecommerce.pages.DashboardPage import DashboardPage


from Selenium_Ecommerce.utils.data_loader import load_test_data


@pytest.fixture
def login_fixture(setup):
    driver = setup
    login_page = LoginPage(driver)
    driver.get("https://admin-demo.nopcommerce.com/login?ReturnUrl=%2Fadmin%2F")
    login_page.login("admin@yourstore.com", "admin")
    dashboard = DashboardPage(driver)
    yield driver, dashboard


@pytest.mark.orders
@allure.feature("Orders Module")
class TestOrdersModule:

    @pytest.fixture(autouse=True)
    def setup_orders(self, setup):
        self.driver = setup
        self.orders_page = OrdersModule(self.driver)
        self.driver.get("https://admin-demo.nopcommerce.com/login?ReturnUrl=%2Fadmin%2F")



        # Login once before navigating to Products (demo admin creds)
        from Selenium_Ecommerce.pages.LoginPage import LoginPage
        login = LoginPage(self.driver)
        login.login("admin@yourstore.com", "admin")

        self.orders_page.go_to_orders()



    @pytest.mark.parametrize("order_id", ["1", "2", "4", "5"])
    @allure.story("Verify Order Status (Cancelled / Pending / Processing / Complete)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_verify_order_status(self, order_id):
        """Enter Order ID, click Go, and assert order status."""
        status = self.orders_page.verify_order_status(order_id)
        assert status in ["Pending", "Processing", "Complete","Cancelled"], (
            f" Invalid status for order {order_id}: {status}"
        )
        print(f" Verified order {order_id} status successfully: {status}")

    @pytest.mark.parametrize("case", load_test_data("Selenium_Ecommerce/utils/data/order_data.csv"))
    @allure.story("Search Orders by Email (Positive & Negative)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_order_by_email(self, case):
         email, expected = case["email"], case["expected"]
         result = self.orders_page.search_by_email(email)
         if expected == "Pass":
             assert result, f"Expected orders for email {email}."
         else:
             assert not result, f"No orders should be found for {email}."

    @pytest.mark.parametrize("case", load_test_data("Selenium_Ecommerce/utils/data/order_data.xml"))
    @allure.story("Search Orders by Last Name (Positive & Negative)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_order_by_last_name(self, case):
         last_name, expected = case["last_name"], case["expected"]
         result = self.orders_page.search_by_last_name(last_name)
         if expected == "Pass":
             assert result, f"Expected orders for last name {last_name}."
         else:
             assert not result, f"No orders should be found for {last_name}."


