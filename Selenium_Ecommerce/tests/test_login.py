
# pytest Selenium_Ecommerce/tests/test_login.py -v -s --clean-alluredir --alluredir=Selenium_Ecommerce/Output/reports/report-login/allure-results --html=Selenium_Ecommerce/Output/reports/report-login/login_report.html --self-contained-html
# allure generate Selenium_Ecommerce/Output/reports/report-login/allure-results -o Selenium_Ecommerce/Output/reports/report-login/allure-report --clean
# allure open Selenium_Ecommerce/Output/reports/report-login/allure-report
# allure serve Selenium_Ecommerce/reports/report-login/allure-results



import allure
import pytest
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# Page Object imports
from Selenium_Ecommerce.pages.LoginPage import LoginPage
from Selenium_Ecommerce.pages.DashboardPage import DashboardPage
# Data loader to support CSV, Excel, XML test data
from Selenium_Ecommerce.utils.data_loader import load_test_data





# ---------------------------------------------------------------
# Login Test Class — Uses Allure Reporting and Screenshot Capture
# ---------------------------------------------------------------
@pytest.mark.login
@allure.feature("Login Module")
class TestLoginLogout:

    # -----------------------------------------------------------
    # Data-Driven Login Test (CSV / XLSX / XML selectable)
    # -----------------------------------------------------------
    @pytest.mark.parametrize("case", load_test_data("Selenium_Ecommerce/utils/data/login_data.xml"))
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.loginnop
    @allure.story("Data Driven Login Test with Allure & Screenshots")
    def test_login_ddt(self, case, setup):
        """
        Attempts to log in with each dataset entry.
        Supports multiple browsers and data formats.
        """
        # Extract fields from dataset
        email, password, expected = case["email"], case["password"], case["expected"]

        driver = setup
        login_page = LoginPage(driver)
        driver.get("https://admin-demo.nopcommerce.com/login?ReturnUrl=%2Fadmin%2F")

        # Step: Attempt Login
        with allure.step(f"Testing login with: {email or '[EMPTY EMAIL]'} | Expected: {expected}"):
            result = login_page.login(email, password)
            login_page.take_screenshot("test_login", f"attempt_{email or 'empty'}")

        # Step: Validate Result — Successful Login
        if expected == "Pass":
            with allure.step("Verifying successful login outcome"):
                assert result == "success", f"Expected success for {email}, but failed."
                login_page.take_screenshot("test_login", f"success_{email or 'empty'}")
                allure.attach(f"Login success for {email}", name="Login Result", attachment_type=allure.attachment_type.TEXT)
                return

        # Step: Validate Expected Failure Messages
        with allure.step("Checking validation or error messages for expected failure"):
            try:
                # Try client-side validation message
                email_error = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.ID, "Email-error"))
                )
                text = email_error.text.strip()
                print(f" Found client-side validation message: {text}")
                assert "Please enter your email" in text, f"Unexpected message: {text}"
                login_page.take_screenshot("test_login", f"missing_email_{email or 'empty'}")
                return

            except TimeoutException:
                print(" No client-side 'Email-error' message found. Checking server-side error...")

            # Fallback: check server-side error banner
            try:
                error_box = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "div.message-error.validation-summary-errors")
                    )
                )
                msg = error_box.text.strip()
                print(f" Found server-side message: {msg}")
                assert "Login was unsuccessful" in msg or "incorrect" in msg.lower(), f"Unexpected message: {msg}"
                login_page.take_screenshot("test_login", f"server_error_{email or 'empty'}")
                return

            except (TimeoutException, NoSuchElementException):
                print(" No visible validation or error message found.")
                login_page.take_screenshot("test_login", f"no_error_{email or 'empty'}")
                assert False, f"No visible validation or error message for {email}"

        # Step: Handle Unexpected Behavior
        login_page.take_screenshot("test_login", f"unexpected_{email or 'empty'}")
        allure.attach("No expected success or error appeared", name="Unexpected Behavior",
                      attachment_type=allure.attachment_type.TEXT)
        assert False, f"No visible validation or error message for {email}"

    # -----------------------------------------------------------
    # Logout Test After Successful Login
    # -----------------------------------------------------------
    @allure.story("Logout Functionality Validation")
    @allure.severity(allure.severity_level.NORMAL)
    def test_logout_after_login(self, setup):
        """
        Logs in with valid credentials and then logs out.
        Captures screenshots for both actions.
        """
        driver = setup
        driver.get("https://admin-demo.nopcommerce.com/login?ReturnUrl=%2Fadmin%2F")
        login_page = LoginPage(driver)

        with allure.step("Performing login for logout test"):
            result = login_page.login("admin@yourstore.com", "admin")
            login_page.take_screenshot("test_login", "before_logout")
            assert result == "success", "Login failed — cannot test logout."

        dashboard = DashboardPage(driver)
        assert "Dashboard" in dashboard.get_title(), "Dashboard not loaded correctly"

        with allure.step("Executing logout from dashboard"):
            dashboard.logout()
            login_page.take_screenshot("test_login", "after_logout")

        # Verify redirected to login page
        assert "Login" in driver.title or "Your store. Login" in driver.title
