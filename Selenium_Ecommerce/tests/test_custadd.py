# pytest Selenium_Ecommerce/tests/test_custadd.py -v -s -n auto --clean-alluredir --alluredir=Selenium_Ecommerce/Output/reports/report-custadd/allure-results --html=Selenium_Ecommerce/Output/reports/report-custadd/custadd_report.html --self-contained-html
# pytest Selenium_Ecommerce/tests/test_custadd.py -v -s -n auto --alluredir=Selenium_Ecommerce/Output/reports/report-custadd/allure-results --html=Selenium_Ecommerce/Output/reports/report-custadd/custadd_report.html
# allure generate Selenium_Ecommerce/Output/reports/report-custadd/allure-results -o  Selenium_Ecommerce/Output/reports/report-custadd/allure-report --clean
# allure open Selenium_Ecommerce/Output/reports/report-custadd/allure-report
# allure serve Selenium_Ecommerce/Output/reports/report-custadd/allure-results

import time
import allure
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

# Import page objects
from Selenium_Ecommerce.pages.LoginPage import LoginPage
from Selenium_Ecommerce.pages.DashboardPage import DashboardPage
from Selenium_Ecommerce.pages.AddCustomerPage import AddCustomerPage
from Selenium_Ecommerce.pages.SearchCustomerPage import SearchCustomerPage
from Selenium_Ecommerce.utils.data_loader import load_test_data  #  Universal data reader (CSV / XLSX / XML)

# ------------------------------------------------------------------------
# Fixture to initialize the WebDriver for multiple browsers
# ------------------------------------------------------------------------


# ------------------------------------------------------------------------
# Fixture to log into the nopCommerce Admin site
# ------------------------------------------------------------------------
@pytest.fixture
def login_fixture(setup):
    """
    Reusable login fixture that authenticates admin user before running tests.
    """
    driver = setup
    login_page = LoginPage(driver)

    # Open the login page
    driver.get("https://admin-demo.nopcommerce.com/login?ReturnUrl=%2Fadmin%2F")

    # Perform login using admin credentials
    login_page.login("admin@yourstore.com", "admin")

    # Validate that Dashboard loaded successfully
    dashboard = DashboardPage(driver)
    assert dashboard.get_title() == "Dashboard / nopCommerce administration", "Login failed!"
    yield driver, dashboard

# ------------------------------------------------------------------------
# Test Class for Customer Management (Add New Customer)
# ------------------------------------------------------------------------
@pytest.mark.add_customer
@allure.feature("Customer Module")
class TestAddCustomer:
    """
    Contains test cases for adding customers.
    Includes data-driven tests (from CSV/XLSX/XML) and random entry test.
    """

    # Automatically setup for all tests in this class
    @pytest.fixture(autouse=True)
    def setup_add(self, login_fixture):
        self.driver, self.dashboard = login_fixture
        self.dashboard.go_to_customers()
        self.add_page = AddCustomerPage(self.driver)
        self.search_page = SearchCustomerPage(self.driver)

    # --------------------------------------------------------------------
    # Data-Driven Test: Add Customer (CSV / XLSX / XML selectable)
    # --------------------------------------------------------------------
    @pytest.mark.parametrize("case", load_test_data("Selenium_Ecommerce/utils/data/customer_data.csv"))
    @allure.story("Add Customer via File Data (CSV/XLSX/XML)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_customer(self, case):
        """
        Adds new customers using input data from external test files.
        Automatically captures screenshots and attaches to Allure.
        """
        first_name, last_name, email, password = (
            case["first_name"], case["last_name"], case["email"], case["password"]
        )

        with allure.step(f"Adding customer: {first_name} {last_name} ({email})"):
            result = self.add_page.add_customer(first_name, last_name, email, password)
            if not result:
                self.add_page.take_screenshot("test_custadd", f"add_fail_{email}")
            assert result, f"Failed to fill or submit Add Customer form for {email}"

        with allure.step("Validating alert after customer creation"):
            alert = self.add_page.get_alert_message()
            if alert not in ["success", "exists"]:
                self.add_page.take_screenshot("test_custadd", f"unexpected_{email}")
            assert alert in ["success", "exists"], f"Unexpected alert: {alert}"

        if alert == "success":
            screenshot = self.add_page.take_screenshot("test_custadd", f"success_{email}")
            allure.attach.file(screenshot, name=f"Customer_{email}_Success", attachment_type=allure.attachment_type.PNG)
            print(f" Customer '{email}' added successfully.")
        elif alert == "exists":
            screenshot = self.add_page.take_screenshot("test_custadd", f"success_{email}")
            allure.attach.file(screenshot, name=f"Customer_{email}_Success", attachment_type=allure.attachment_type.PNG)
            print(f" Customer '{email}' already exists.")

    # --------------------------------------------------------------------
    # Dynamic Test: Add Random Customer (Unique email each run)
    # --------------------------------------------------------------------
    @allure.story("Add Randomly Generated Customer")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_customer_from_user(self):
        """
        Adds a new customer with randomly generated email.
        Used to verify that customer creation works end-to-end.
        """
        # Generate random unique data
        first_name, last_name = "Anu", "Singh"
        email = f"{first_name.lower()}.{last_name.lower()}{int(time.time())}@example.com"
        password = "Pwd@1234"

        with allure.step(f"Adding random customer {email}"):
            add_result = self.add_page.add_customer(first_name, last_name, email, password)
            assert add_result, " Failed to fill or submit the Add Customer form."

            # Step : Check alert message after submission
            alert_result = self.add_page.get_alert_message()
            if alert_result == "success":
                screenshot = self.add_page.take_screenshot("test_custadd", f"success_{email}")
                allure.attach.file(screenshot, name=f"Customer_{email}_Success",
                                   attachment_type=allure.attachment_type.PNG)
                print(f" Customer '{email}' added successfully.")
            elif alert_result == "exists":
                screenshot = self.add_page.take_screenshot("test_custadd", f"success_{email}")
                allure.attach.file(screenshot, name=f"Customer_{email}_Success",
                                   attachment_type=allure.attachment_type.PNG)
                print(f" Customer '{email}' already exists.")
            else:
                screenshot = self.add_page.take_screenshot("test_custadd", f"failed_{email}")
                allure.attach.file(screenshot, name=f"Customer_{email}_Failed",
                                   attachment_type=allure.attachment_type.PNG)
                assert False, f"Add Customer failed for {email}"
