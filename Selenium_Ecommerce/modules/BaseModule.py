
import os
import shutil
import time

import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

class BaseModule:
    """
    BasePage: common helpers used across page objects. All common Selenium
    interactions and the screenshot / allure attachment helper live here.


    Comments: Keep waits centralized so changes here affect all pages.
    """
    _cleaned_folders = set()



    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def login(self, username, password):
        self.navigate_to_login()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def navigate_to_login(self):
        self.driver.get("https://admin-demo.nopcommerce.com/")
        time.sleep(1)

    def enter_username(self, username):
        field = self.driver.find_element(By.ID, "Email")
        field.clear()
        field.send_keys(username)

    def enter_password(self, password):
        field = self.driver.find_element(By.ID, "Password")
        field.clear()
        field.send_keys(password)

    def click_login(self):
        self.driver.find_element(By.XPATH, "//button[normalize-space()='Log in']").click()
        time.sleep(2)

    def click_element(self, by, locator):
        """Wait for an element to be clickable, then click."""
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((by, locator))).click()

    def enter_text(self, by, locator, text):
        """Clear and enter text into an input field."""
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((by, locator)))
        element.clear()
        element.send_keys(text)

    def get_title(self):
        return self.driver.title

    def is_element_present(self, locator):
        try:
            self.wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def wait_not_present(self, locator, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until_not(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def wait_for_element_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def safe_click(self, locator):
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
        except Exception:
            element = self.driver.find_element(*locator)
            self.driver.execute_script("arguments[0].click();", element)



    def take_screenshot(self, folder_name="general", name_prefix="screenshot"):
        """
         Takes a screenshot and saves it in:
            Selenium_Ecommerce/screenshots/<folder_name>/

         Cleans the folder ONCE per test run (per test file),
        so old screenshots are deleted only at the first capture of the test.
        """

        screenshot_dir = os.path.join(os.getcwd(), "Selenium_Ecommerce", "Output", "screenshots", folder_name)

        # Clean only once per folder per test run
        if folder_name not in self._cleaned_folders:
            if os.path.exists(screenshot_dir):
                print(f" Cleaning old screenshots in: {screenshot_dir}")
                shutil.rmtree(screenshot_dir)  # Delete entire folder
            os.makedirs(screenshot_dir, exist_ok=True)
            self._cleaned_folders.add(folder_name)

        # Generate new screenshot file
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(screenshot_dir, f"{name_prefix}_{timestamp}.png")

        # Save screenshot
        self.driver.save_screenshot(file_path)
        print(f" Screenshot saved: {file_path}")

        return file_path

    @allure.step("Scrolling to element")
    def scroll_to_element(self, by, locator):
        """Scrolls to the element before interacting (works across browsers)."""
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((by, locator))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            print(f"  Scrolled to element: {locator}")
            return element
        except TimeoutException:
            print(f" Timeout: Could not scroll to element: {locator}")
        except Exception as e:
            print(f" Could not scroll to element: {locator} | Error: {e}")

    def clear_and_type(self, by, locator, text):
        """
        Wait for a text box, clear existing content, and type new text safely.
        Works reliably across Chrome, Edge, and Firefox.
        """
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((by, locator))
            )
            element.clear()
            element.send_keys(text)
            print(f" Entered text '{text}' into element: {locator}")
        except TimeoutException:
            print(f" Timeout: Unable to locate element {locator} for typing.")
            raise
        except Exception as e:
            print(f" Error while entering text into {locator}: {e}")
            raise

    def get_error_message(self):
        try:
            return self.driver.find_element(By.CSS_SELECTOR, ".message-error").text
        except:
            return None

    def is_login_successful(self):
        try:
            return "Dashboard" in self.driver.title
        except:
            return False

    def logout(self):
        try:
            self.driver.find_element(By.XPATH, "//a[normalize-space()='Logout']").click()
            time.sleep(1)
            return True
        except:
            return False

    def scroll_into_view(self, element):
        """Scroll the page so that the given element is visible."""
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            print(f" Scrolled to element: {element}")
            time.sleep(0.5)  # small pause to ensure stability
        except Exception as e:
            print(f" Could not scroll to element: {e}")

