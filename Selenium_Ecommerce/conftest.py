import shutil

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from Selenium_Ecommerce.pages.LoginPage import LoginPage
from Selenium_Ecommerce.pages.DashboardPage import DashboardPage

# Selenium Grid URL
GRID_URL = "http://localhost:4444/wd/hub"

# ------------------------------------------------------------------
#  Pytest CLI options
# ------------------------------------------------------------------
import tempfile



def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chrome,firefox,edge", help="Browser to use: chrome, edge, firefox"
    )
    parser.addoption(
        "--grid", action="store_true", help="Run tests on Selenium Grid"
    )
    parser.addoption(
        "--headless", action="store_true", help="Run tests in headless mode"
    )
    parser.addoption(
        "--all-browsers", action="store_true", help="Run on all supported browsers"
    )

# ------------------------------------------------------------------
#  Generate tests dynamically based on browser list
# ------------------------------------------------------------------
def pytest_generate_tests(metafunc):
    if "setup" in metafunc.fixturenames:
        browsers = [b.strip() for b in metafunc.config.getoption("browser").split(",") if b.strip()]
        metafunc.parametrize("setup", browsers, indirect=True)


# ------------------------------------------------------------------
#  Browser Fixture
# ------------------------------------------------------------------
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
        user_data_dir = tempfile.mkdtemp()
        options.add_argument(f"--user-data-dir={user_data_dir}")
        if headless:
            options.add_argument("--headless=new")

        driver = (
            webdriver.Remote(command_executor=GRID_URL, options=options)
            if use_grid
            else webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()), options=options
            )
        )

    elif browser.lower() == "firefox":
        options = FirefoxOptions()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        options.add_argument("--disable-gpu")
        user_data_dir = tempfile.mkdtemp(prefix="selenium_profile_")# create a unique temp directory
        options.add_argument(f"--user-data-dir={user_data_dir}")

        if headless:
            options.add_argument("--headless")

        driver = (
            webdriver.Remote(command_executor=GRID_URL, options=options)
            if use_grid
            else webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()), options=options
            )
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
        user_data_dir = tempfile.mkdtemp()
        options.add_argument(f"--user-data-dir={user_data_dir}")
        if headless:
            options.add_argument("--headless=new")

        driver = (
            webdriver.Remote(command_executor=GRID_URL, options=options)
            if use_grid
            else webdriver.Edge(
                #service=EdgeService("C:/Drivers/msedgedriver.exe"), options=options
                service=EdgeService(EdgeChromiumDriverManager().install()), options=options
            )
        )

    else:
        raise ValueError(f" Unsupported browser: {browser}")

    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()
    shutil.rmtree(user_data_dir, ignore_errors=True)

# ------------------------------------------------------------------
#  Login Fixture
# ------------------------------------------------------------------
@pytest.fixture
def login_fixture(setup):
    """Reusable fixture for admin login"""
    driver = setup
    login_page = LoginPage(driver)
    driver.get("https://admin-demo.nopcommerce.com/login?ReturnUrl=%2Fadmin%2F")
    login_page.login("admin@yourstore.com", "admin")

    dashboard = DashboardPage(driver)
    assert "Dashboard" in dashboard.get_title()
    yield driver, dashboard
