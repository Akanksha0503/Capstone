# from selenium.webdriver import ActionChains
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.common.exceptions import TimeoutException, NoSuchElementException
# from Selenium_Ecommerce.modules.BaseModule import BaseModule
#
# from selenium.webdriver.support import expected_conditions as EC
#
#
# class LoginPage(BaseModule):
#     EMAIL_FIELD = (By.ID, "Email")
#     PASSWORD_FIELD = (By.ID, "Password")
#     LOGIN_BUTTON = (By.XPATH, "//button[contains(text(),'Log in')]")
#     LOGOUT_LINK = (By.XPATH, "//a[contains(text(),'Logout')]")
#     remember_me_checkbox = (By.ID, "RememberMe")
#
#     #  exact invalid message div from your HTML
#     ERROR_DIV = (By.XPATH, "//div[@class='message-error validation-summary-errors']")
#
#     def __init__(self, driver):
#         super().__init__(driver)
#         self.wait = WebDriverWait(driver, 10)
#
#     def login(self, email, password):
#         """Attempts login; returns 'success', 'invalid', or 'none'."""
#         global email_field, password_field
#         print(f" Trying login: {email or '[EMPTY EMAIL]'} / {password or '[EMPTY PASSWORD]'}")
#
#         # Ensure page fully loaded
#         for attempt in range(2):
#             try:
#                 self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
#                 email_field = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
#                 password_field = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
#                 break
#             except TimeoutException:
#                 print(f"Attempt {attempt + 1}: Page/elements not ready, refreshing...")
#                 self.driver.refresh()
#                 if attempt == 1:
#                     self.take_screenshot("test_login", "login_page_not_ready")
#                     return "none"
#
#         email_field.clear()
#         email_field.send_keys(email)
#         password_field.clear()
#         password_field.send_keys(password)
#
#         # Handle 'Remember Me'
#         try:
#             remember_me = self.driver.find_element(*self.remember_me_checkbox)
#             if not remember_me.is_selected():
#                 remember_me.click()
#         except NoSuchElementException:
#             print(" 'Remember Me' checkbox not found — continuing anyway.")
#
#         # Wait for login button to be clickable and click via JS fallback
#         try:
#             login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
#             self.driver.execute_script("arguments[0].scrollIntoView(true);", login_btn)
#             try:
#                 login_btn.click()
#                 print(" Clicked the Login button successfully (normal click).")
#             except:
#                 # JS fallback click if normal click fails
#                 self.driver.execute_script("arguments[0].click();", login_btn)
#                 print(" Clicked the Login button successfully (JS fallback).")
#         except Exception as e:
#             print(f" Failed to click the Login button: {e}")
#             self.take_screenshot("test_login", "login_click_error.png")
#             return "none"
#
#         # Wait for Dashboard or error message
#         try:
#             self.wait.until(
#                 lambda d: "Dashboard" in d.title or d.find_elements(*self.ERROR_DIV)
#             )
#         except TimeoutException:
#             print(" Timeout: neither Dashboard nor error message appeared.")
#             self.take_screenshot("test_login", "dashboard_not_loaded.png")
#             return "none"
#
#         # Success Case
#         if "Dashboard" in self.driver.title:
#             print(" Login successful.")
#             return "success"
#
#         # Invalid Login Case
#         elif self.is_element_present(self.ERROR_DIV):
#             error_text = self.driver.find_element(*self.ERROR_DIV).text.strip()
#             print(f" Login failed. Error text: {error_text}")
#             return "invalid"
#
#         # Unexpected Case
#         else:
#             print(" Unexpected login result.")
#             self.take_screenshot("test_login", "unexpected_result.png")
#             return "none"
#
#     def logout(self):
#         """Logs out from the system."""
#         try:
#             # Wait up to 10 seconds for the logout link to be clickable
#             logout_btn = WebDriverWait(self.driver, 10).until(
#                 EC.element_to_be_clickable(self.LOGOUT_LINK)
#             )
#
#             # Scroll into view
#             self.driver.execute_script("arguments[0].scrollIntoView(true);", logout_btn)
#
#             # Try normal click first
#             try:
#                 logout_btn.click()
#                 print(" Logged out successfully (normal click).")
#             except:
#                 # Fallback to JS click
#                 self.driver.execute_script("arguments[0].click();", logout_btn)
#                 print(" Logged out successfully (JS fallback click).")
#
#         except TimeoutException:
#             print(" Logout failed — 'Logout' link not clickable or not found.")
#             self.take_screenshot("test_logout", "logout_not_clickable.png")
#         except Exception as e:
#             print(f" Logout failed: {e}")
#             self.take_screenshot("test_logout", "logout_error.png")
#
#
#
import os
import time
from selenium.webdriver import ActionChains
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

    def wait_for_login_form(driver, timeout=20):
        """Wait until login form fields are visible and enabled."""
        email_field = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.ID, "Email"))
        )
        password_field = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.ID, "Password"))
        )
        login_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        return email_field, password_field, login_button
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
            print(f" Logout error: {e}")
            self.take_screenshot("test_logout", "logout_error")
