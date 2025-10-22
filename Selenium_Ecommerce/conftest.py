#
# from Selenium_Ecommerce.pages.DashboardPage import DashboardPage
# from Selenium_Ecommerce.pages.LoginPage import LoginPage
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.edge.options import Options as EdgeOptions
# from selenium.webdriver.edge.service import Service as EdgeService
#
# import pytest
#
# GRID_URL = "http://localhost:4444/wd/hub"
#
# def pytest_addoption(parser):
#     parser.addoption(
#         "--browser", action="store", default="chrome,firefox,edge", help="Browser to use: chrome, edge, firefox"
#     )
#     parser.addoption(
#         "--grid", action="store_true", help="Run tests on Selenium Grid"
#     )
#     parser.addoption(
#         "--headless", action="store_true", help="Run tests in headless mode"
#     )
#     parser.addoption(
#         "--all-browsers", action="store_true", help="Run on all supported browsers"
#     )
#
# def pytest_generate_tests(metafunc):
#     if "setup" in metafunc.fixturenames:
#         browsers = [b.strip() for b in metafunc.config.getoption("browser").split(",") if b.strip()]
#         metafunc.parametrize("setup", browsers, indirect=True)
#
# @pytest.fixture()
# def setup(request):
#     browser = request.param
#     use_grid = request.config.getoption("--grid")
#     headless = request.config.getoption("--headless")
#
#     if browser == "chrome":
#         options = webdriver.ChromeOptions()
#         options.add_argument("--no-sandbox")
#         options.add_argument("--disable-dev-shm-usage")
#         options.add_argument("--disable-gpu")
#         options.add_argument("--window-size=1920,1080")
#         options.add_argument("--disable-extensions")
#         options.add_argument("--disable-infobars")
#         options.add_argument("--remote-debugging-port=9222")
#         options.add_argument("--ignore-certificate-errors")
#         options.add_argument("--disable-blink-features=AutomationControlled")
#         options.add_argument(
#             "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.7339.207 Safari/537.36"
#         )
#
#         if headless:
#             options.add_argument("--headless=new")
#
#         driver = (
#             webdriver.Remote(command_executor=GRID_URL, options=options)
#             if use_grid
#             else webdriver.Chrome(
#                 service=ChromeService(ChromeDriverManager().install()), options=options
#             )
#         )
#
#     elif browser == "firefox":
#         from selenium.webdriver.firefox.service import Service as FirefoxService
#         from webdriver_manager.firefox import GeckoDriverManager
#         options = webdriver.FirefoxOptions()
#
#         options.add_argument("--width=1920")
#         options.add_argument("--height=1080")
#         if headless:
#             options.add_argument("--headless")
#
#         driver_path = r"C:\Users\Ascendion\.wdm\drivers\geckodriver\win64\v0.36.0\geckodriver.exe"
#
#         driver = (
#             webdriver.Remote(command_executor=GRID_URL, options=options)
#             if use_grid
#             else webdriver.Firefox(
#                 service=FirefoxService(driver_path), options=options
#             )
#         )
#     elif browser.lower() == "edge":
#         options = EdgeOptions()
#         options.add_argument("--no-sandbox")
#         options.add_argument("--disable-dev-shm-usage")
#         options.add_argument("--disable-gpu")
#         options.add_argument("--disable-extensions")
#         options.add_argument("--disable-infobars")
#         options.add_argument("--window-size=1920,1080")
#
#         if headless:
#             options.add_argument("--headless=new")
#
#         driver = (
#             webdriver.Remote(command_executor=GRID_URL, options=options)
#             if use_grid
#             else webdriver.Edge(
#                 service=EdgeService("C:/Drivers/msedgedriver.exe"), options=options
#                 # service=EdgeService(EdgeChromiumDriverManager().install()), options=options
#             )
#         )
#     else:
#         raise ValueError(f"Unsupported browser: {browser}")
#
#     driver.set_page_load_timeout(40)
#     driver.implicitly_wait(10)
#     driver.maximize_window()
#     driver.get("https://admin-demo.nopcommerce.com/login?ReturnUrl=%2Fadmin%2F")
#
#     request.cls.driver = driver
#     yield driver
#     driver.quit()
#
#
# # ------------------------------------------------------------------
# #  Login Fixture
# # ------------------------------------------------------------------
# @pytest.fixture
# def login_fixture(setup):
#     """Reusable fixture for admin login"""
#     driver = setup
#     login_page = LoginPage(driver)
#     driver.get("https://admin-demo.nopcommerce.com/login?ReturnUrl=%2Fadmin%2F")
#
#
#     login_page.login("admin@yourstore.com", "admin")
#
#     dashboard = DashboardPage(driver)
#     assert "Dashboard" in dashboard.get_title()
#     yield driver, dashboard

import os

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

@pytest.fixture(params=["chrome", "firefox"], scope="class")
def setup(request):
    """
    Fixture to initialize local Chrome or Firefox driver.
    Detects GitHub Actions for headless mode.
    """
    browser = request.param
    headless = os.getenv("GITHUB_ACTIONS") == "true"

    driver = None

    if browser.lower() == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--start-maximized")
        if headless:
            options.add_argument("--headless=new")

        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    elif browser.lower() == "firefox":
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("--headless")
            options.add_argument("--start-maximized")


        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
        timeout=300
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.set_page_load_timeout(60)
    driver.implicitly_wait(10)

    request.cls.driver = driver
    yield driver
    driver.quit()
# Attach screenshots on failure to Allure report

