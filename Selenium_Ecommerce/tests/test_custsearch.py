# pytest Selenium_Ecommerce/tests/test_custsearch.py -v -s -n auto --clean-alluredir --alluredir=Selenium_Ecommerce/Output/reports/report-custsearch/allure-results --html=Selenium_Ecommerce/Output/reports/report-custsearch/custsearch_report.html --self-contained-html
# allure generate Selenium_Ecommerce/Output/reports/report-custsearch/allure-results -o Selenium_Ecommerce/Output/reports/report-custsearch/allure-report --clean
# allure open Selenium_Ecommerce/Output/reports/report-custsearch/allure-report
# allure serve Selenium_Ecommerce/Output/reports/report-custsearch/allure-results

#pytest Selenium_Ecommerce/tests/test_products.py -n auto --browser chrome,firefox --grid --headless -v -s

#pytest Selenium_Ecommerce/tests/test_custsearch.py --browser chrome,edge --grid --headless -v -s
import pytest
import allure

from Selenium_Ecommerce.pages.DashboardPage import DashboardPage
from Selenium_Ecommerce.pages.SearchCustomerPage import SearchCustomerPage
from Selenium_Ecommerce.utils.data_loader import load_test_data  #  New


# ------------------------------------------------------------------------
# Test Class for Searching Customers
# ------------------------------------------------------------------------

@pytest.mark.search
@allure.feature("Customer Module")
class TestSearchCustomer:
    """
        Validates customer search functionality using email and full name.
        Supports data-driven testing from CSV / XLSX / XML.
        """
    @pytest.fixture(autouse=True)
    def setup_search(self, login_fixture):
        self.driver, self.dashboard = login_fixture

        self.search_page = SearchCustomerPage(self.driver)
        self.dashboard = DashboardPage(self.driver)
        self.driver.get("https://admin-demo.nopcommerce.com/login?ReturnUrl=%2Fadmin%2F")

        # Login once before navigating to Products (demo admin creds)
        from Selenium_Ecommerce.pages.LoginPage import LoginPage
        login = LoginPage(self.driver)
        login.login("admin@yourstore.com", "admin")

        self.dashboard.go_to_customers()

    # --------------------------------------------------------------------
    # Test  — Search by Email
    # --------------------------------------------------------------------
    @pytest.mark.parametrize("email", ["admin@yourstore.com"])
    @allure.story("Search by Email")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_by_email(self, email):
        """
                Verifies that a customer can be found by registered email.
                """
        with allure.step(f"Searching by email: {email}"):
            result = self.search_page.search_by_email(email)
            assert result, f"Email '{email}' not found in results."

            #  Capture screenshot for successful case
            screenshot = self.search_page.take_screenshot("test_custsearch", f"email_found_{email}")
            allure.attach.file(
                screenshot,
                name=f"Customer_Email_{email}_Success",
                attachment_type=allure.attachment_type.PNG,
            )
            print(f" Customer with email '{email}' found successfully.")

        # --------------------------------------------------------------------
        #  Search by First Name (Data-driven)
        # --------------------------------------------------------------------

    @pytest.mark.parametrize("case", load_test_data("Selenium_Ecommerce/utils/data/customer_data.xlsx"))
    @allure.story("Search by First Name")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_by_first_name(self, case):
        """Verifies customer search by First Name."""
        first_name = case["first_name"]
        with allure.step(f"Searching by first name: {first_name}"):
            result = self.search_page.search_by_first_name(first_name)
            assert result, f"Customer with first name '{first_name}' not found."

            screenshot = self.search_page.take_screenshot("test_custsearch", f"first_name_found_{first_name}")
            allure.attach.file(
                screenshot,
                name=f"Customer_FirstName_{first_name}_Success",
                attachment_type=allure.attachment_type.PNG,
            )
            print(f" Customer with first name '{first_name}' found successfully.")

    # --------------------------------------------------------------------
    # Search by Last Name (Data-driven)
    # --------------------------------------------------------------------
    @pytest.mark.parametrize("case", load_test_data("Selenium_Ecommerce/utils/data/customer_data.xml"))
    @allure.story("Search by Last Name")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_by_last_name(self, case):
        """Verifies customer search by Last Name."""
        last_name = case["last_name"]
        with allure.step(f"Searching by last name: {last_name}"):
            result = self.search_page.search_by_last_name(last_name)
            assert result, f"Customer with last name '{last_name}' not found."

            screenshot = self.search_page.take_screenshot("test_custsearch", f"last_name_found_{last_name}")
            allure.attach.file(
                screenshot,
                name=f"Customer_LastName_{last_name}_Success",
                attachment_type=allure.attachment_type.PNG,
            )
            print(f" Customer with last name '{last_name}' found successfully.")

    # --------------------------------------------------------------------
    # Search by Role (Data-driven)
    # --------------------------------------------------------------------
    @pytest.mark.parametrize("case", load_test_data("Selenium_Ecommerce/utils/data/rolescustomer_data.csv"))
    @allure.story("Search by Role")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_by_role(self, case):
        """Verifies customer search by Role."""
        role_name = case.get("role")  # Ensure your XML has <role> entries
        if not role_name:
            pytest.skip("No role provided in test data.")

        with allure.step(f"Searching by role: {role_name}"):
            result = self.search_page.search_by_role(role_name)
            assert result, f"Customer with role '{role_name}' not found."

            screenshot = self.search_page.take_screenshot("test_custsearch", f"role_found_{role_name}")
            allure.attach.file(
                screenshot,
                name=f"Customer_Role_{role_name}_Success",
                attachment_type=allure.attachment_type.PNG,
            )
            print(f" Customer with role '{role_name}' found successfully.")