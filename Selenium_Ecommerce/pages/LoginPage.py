from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from Selenium_Ecommerce.modules.BaseModule import BaseModule


class LoginPage(BaseModule):
    EMAIL_FIELD = (By.ID, "Email")
    PASSWORD_FIELD = (By.ID, "Password")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(),'Log in')]")
    LOGOUT_LINK = (By.XPATH, "//a[contains(text(),'Logout')]")

    #  exact invalid message div from your HTML
    ERROR_DIV = (By.XPATH, "//div[@class='message-error validation-summary-errors']")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 10)

    def login(self, email, password):
        """Attempts login; returns 'success', 'invalid', or 'none'."""
        print(f" Trying login: {email} / {password}")
        self.enter_text(*self.EMAIL_FIELD, email)
        self.enter_text(*self.PASSWORD_FIELD, password)
        self.click_element(*self.LOGIN_BUTTON)

        try:
            # Wait for either Dashboard or error message
            self.wait.until(
                lambda driver: "Dashboard" in driver.title
                or driver.find_elements(*self.ERROR_DIV)
            )
        except TimeoutException:
            print(" Neither Dashboard nor error message appeared — timeout.")
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
            self.click_element(self.LOGOUT_LINK)
            print(" Logged out successfully.")
        except Exception:
            print(" Logout failed — element not found.")


