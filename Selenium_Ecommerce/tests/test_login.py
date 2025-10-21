import time

# pytest Selenium_Ecommerce/tests/test_login.py -v -s --clean-alluredir --alluredir=Selenium_Ecommerce/Output/reports/report-login/allure-results --html=Selenium_Ecommerce/Output/reports/report-login/login_report.html --self-contained-html
# allure generate Selenium_Ecommerce/Output/reports/report-login/allure-results -o Selenium_Ecommerce/Output/reports/report-login/allure-report --clean
# allure open Selenium_Ecommerce/Output/reports/report-login/allure-report
# allure serve Selenium_Ecommerce/reports/report-login/allure-results



import allure
import pytest
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

# Page Object imports
from Selenium_Ecommerce.pages.LoginPage import LoginPage
from Selenium_Ecommerce.pages.DashboardPage import DashboardPage
# Data loader to support CSV, Excel, XML test data
from Selenium_Ecommerce.utils.data_loader import load_test_data



@pytest.fixture
def setup(request):
    browser = request.param
    use_grid = request.config.getoption("--grid")
    headless = request.config.getoption("--headless")

    driver = None

    if browser.lower() == "chrome":
        options = ChromeOptions()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        if headless:
            options.add_argument("--headless=new")

        driver =  webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()), options=options
            )


    elif browser.lower() == "firefox":
        options = FirefoxOptions()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        options.add_argument("--disable-gpu")

        if headless:
            options.add_argument("--headless")

        driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()), options=options
            )

        # if headless:
        #     options.add_argument("--headless")
        #
        # driver_path = r"C:\Users\Ascendion\.wdm\drivers\geckodriver\win64\v0.36.0\geckodriver.exe"
        #
        # driver = (
        #     webdriver.Remote(command_executor=GRID_URL, options=options)
        #     if use_grid
        #     else webdriver.Firefox(
        #         service=FirefoxService(driver_path), options=options
        #     )
        # )

    elif browser.lower() == "edge":
        options = EdgeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--window-size=1920,1080")

        if headless:
            options.add_argument("--headless=new")

        driver = webdriver.Edge(
                service=EdgeService("C:/Drivers/msedgedriver.exe"), options=options
                #service=EdgeService(EdgeChromiumDriverManager().install()), options=options
            )


    else:
        raise ValueError(f" Unsupported browser: {browser}")

    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

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
