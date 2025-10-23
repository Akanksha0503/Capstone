
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from Selenium_Ecommerce.modules.BaseModule import BaseModule


class LoginPage(BaseModule):
    EMAIL_FIELD = (By.ID, "Email")
    PASSWORD_FIELD = (By.ID, "Password")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(),'Log in')]")
    LOGOUT_LINK = (By.XPATH, "//a[contains(text(),'Logout')]")
    REMEMBER_ME = (By.ID, "RememberMe")
    ERROR_DIV = (By.CSS_SELECTOR, "div.message-error.validation-summary-errors")

    def __init__(self, driver):
        super().__init__(driver)
        # Increased default wait for CI reliability
        self.wait = WebDriverWait(driver, 20)

    def wait_for_form_ready(self, max_attempts=3):
        """Wait until the login form is fully ready."""
        for attempt in range(max_attempts):
            try:
                self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
                self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
                self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
                print(f"Login form ready on attempt {attempt + 1}")
                return True
            except TimeoutException:
                print(f" Attempt {attempt + 1}: Login form not ready, refreshing...")
                self.take_screenshot("test_login", f"login_page_not_ready_attempt{attempt + 1}")
                self.driver.refresh()
                time.sleep(2 * (attempt + 1))
        return False

    def login(self, email, password):
        """Attempts login; returns one of:
           'success', 'invalid_email', 'no_account', 'wrong_credentials', or 'none'."""
        print(f" Trying login: {email or '[EMPTY EMAIL]'} / {password or '[EMPTY PASSWORD]'}")

        dashboard_url = "https://admin-demo.nopcommerce.com/admin/"
        email_error_elem = (By.ID, "Email-error")
        error_div_elem = (By.CSS_SELECTOR, "div.message-error.validation-summary-errors")

        # Ensure login form is ready
        if not self.wait_for_form_ready():
            return "none"

        # Fill credentials
        email_field = self.driver.find_element(*self.EMAIL_FIELD)
        password_field = self.driver.find_element(*self.PASSWORD_FIELD)
        email_field.clear()
        email_field.send_keys(email)
        password_field.clear()
        password_field.send_keys(password)

        # Toggle "Remember Me" checkbox
        try:
            remember_me = self.driver.find_element(*self.REMEMBER_ME)
            if not remember_me.is_selected():
                remember_me.click()
        except NoSuchElementException:
            print(" Remember Me checkbox not found — skipping.")

        # Click the Login button
        try:
            login_btn = self.driver.find_element(*self.LOGIN_BUTTON)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", login_btn)
            try:
                login_btn.click()
                print(" Clicked Login button.")
            except:
                self.driver.execute_script("arguments[0].click();", login_btn)
                print(" Clicked Login button (JS fallback).")
        except Exception as e:
            print(f" Login button click failed: {e}")
            self.take_screenshot("test_login", "login_click_error")
            return "none"

        # Wait for either success or failure outcome
        timeout = 25
        poll_interval = 1
        end_time = time.time() + timeout

        while time.time() < end_time:
            current_url = self.driver.current_url

            #  Success case: Dashboard loaded
            if current_url.strip("/") == dashboard_url.strip("/"):
                print(" Login successful — Dashboard loaded.")
                return "success"

            #  Client-side validation: Missing email
            try:
                email_err = self.driver.find_element(*email_error_elem)
                if email_err.is_displayed() and "Please enter your email" in email_err.text:
                    print(f" Validation error: {email_err.text.strip()}")
                    self.take_screenshot("test_login", "invalid_email")
                    return "invalid_email"
            except NoSuchElementException:
                pass

            #  Server-side errors
            try:
                err_block = self.driver.find_element(*error_div_elem)
                if err_block.is_displayed():
                    msg = err_block.text.strip()
                    print(f" Server error detected: {msg}")
                    self.take_screenshot("test_login", "login_error")
                    if "No customer account found" in msg:
                        return "no_account"
                    elif "The credentials provided are incorrect" in msg:
                        return "wrong_credentials"
                    else:
                        return "invalid"
            except NoSuchElementException:
                pass

            time.sleep(poll_interval)

        # Timeout fallback
        print(" Timeout: No known post-login condition detected.")
        self.take_screenshot("test_login", "dashboard_not_loaded")
        return "none"

    def logout(self):
        """Logs out from the system."""
        try:
            logout_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.LOGOUT_LINK))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", logout_btn)
            try:
                logout_btn.click()
                print("Logged out (normal click).")
            except:
                self.driver.execute_script("arguments[0].click();", logout_btn)
                print("Logged out (JS fallback).")
        except TimeoutException:
            print(" Logout link not clickable.")
            self.take_screenshot("test_logout", "logout_not_clickable")
        except Exception as e:
            print(f"Logout error: {e}")
            self.take_screenshot("test_logout", "logout_error")
