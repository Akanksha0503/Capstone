from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from Selenium_Ecommerce.modules.BaseModule import BaseModule

from selenium.webdriver.support import expected_conditions as EC


class LoginPage(BaseModule):
    EMAIL_FIELD = (By.ID, "Email")
    PASSWORD_FIELD = (By.ID, "Password")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(),'Log in')]")
    LOGOUT_LINK = (By.XPATH, "//a[contains(text(),'Logout')]")
    remember_me_checkbox = (By.ID, "RememberMe")

    #  exact invalid message div from your HTML
    ERROR_DIV = (By.XPATH, "//div[@class='message-error validation-summary-errors']")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 10)

    def login(self, email, password):
        """Attempts login; returns 'success', 'invalid', or 'none'."""
        print(f" Trying login: {email or '[EMPTY EMAIL]'} / {password or '[EMPTY PASSWORD]'}")

        # Wait until page fully loads before interacting
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

        try:
            email_field = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
            email_field.clear()
            email_field.send_keys(email)

            password_field = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
            password_field.clear()
            password_field.send_keys(password)
        except TimeoutException:
            print(" Login fields not visible — page may not have loaded correctly.")
            return "none"

        # Handle 'Remember Me'
        try:
            remember_me = self.driver.find_element(*self.remember_me_checkbox)
            if not remember_me.is_selected():
                remember_me.click()
        except NoSuchElementException:
            print(" 'Remember Me' checkbox not found — continuing anyway.")

            # Click the login button
            try:
                self.click_element(*self.LOGIN_BUTTON)
            except Exception as e:
                print(f" Login button click failed: {e}")
                return "none"

            # Wait for Dashboard or error message
            try:
                self.wait.until(
                    lambda d: "Dashboard" in d.title or d.find_elements(*self.ERROR_DIV)
                )
            except TimeoutException:
                print(" Timeout: neither Dashboard nor error message appeared.")
                return "none"
        #  Success Case
        if "Dashboard" in self.driver.title:
            print(" Login successful.")
            return "success"

        #  Invalid Login Case
        elif self.is_element_present(self.ERROR_DIV):
            error_text = self.driver.find_element(*self.ERROR_DIV).text.strip()
            print(f" Login failed. Error text: {error_text}")
            return "invalid"

        #  Unexpected Case
        else:
            print(" Unexpected login result.")
            return "none"

    def logout(self):
        """Logs out from the system."""
        try:
            self.wait.until(EC.element_to_be_clickable(self.LOGOUT_LINK))
            self.click_element(*self.LOGOUT_LINK)
            print(" Logged out successfully.")
        except Exception:
            print(" Logout failed — 'Logout' link not found or not clickable.")


