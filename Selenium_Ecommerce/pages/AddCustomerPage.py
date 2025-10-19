
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from Selenium_Ecommerce.modules.BaseModule import BaseModule


class AddCustomerPage(BaseModule):
    # ----------------------------
    # Locators
    # ----------------------------
    MORE_INFO_LINK = (By.XPATH, "//a[@href='/Admin/Customer/List' and contains(.,'More info')]")
    ADD_CUSTOMER_BUTTON = (By.XPATH, "/html/body/div[3]/div[1]/form[1]/div/div/a")

    FIRST_NAME = (By.ID, "FirstName")
    LAST_NAME = (By.ID, "LastName")
    EMAIL = (By.ID, "Email")
    PASSWORD = (By.ID, "Password")
    SAVE_BUTTON = (By.NAME, "save")

    SUCCESS_MESSAGE = (By.XPATH, "//div[contains(@class, 'alert-success') and contains(text(), 'added successfully')]")
    #EXISTING_EMAIL_ALERT = (By.XPATH, "//form//ul/li[contains(text(), 'Email is already registered')]")
    DUPLICATE_EMAIL_MESSAGE = (By.XPATH, "//li[contains(text(),'Email is already registered')]")

    PAGE_HEADER = (By.XPATH, "//h1[contains(text(), 'Customers')]")

    # ----------------------------
    # Constructor
    # ----------------------------
    def __init__(self, driver):
        super().__init__(driver)

    # ----------------------------
    # Add Customer Flow
    # ----------------------------
    def open_add_customer_form(self):
        """Click the 'Add new' button to open the Add Customer form."""
        print(" Opening 'Add New Customer' form...")

        try:
            # Wait for Customers page header
            self.wait.until(EC.visibility_of_element_located(self.PAGE_HEADER))
        except TimeoutException:
            print(" Customers page header not found. Refreshing page...")
            self.driver.refresh()
            self.wait.until(EC.visibility_of_element_located(self.PAGE_HEADER))

        # Try to find and click Add New button
        try:
            button = self.wait.until(EC.element_to_be_clickable(self.ADD_CUSTOMER_BUTTON))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
            button.click()
            print("Clicked 'Add new' button successfully.")
        except TimeoutException:
            print(" 'Add new' button not found after waiting.")
            raise

    def add_customer(self, first_name, last_name, email, password):
        print(f" Adding customer: {first_name} {last_name} ({email})")

        try:
            add_new_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[@class='btn btn-primary' and contains(.,'Add new')]"))
            )
            add_new_btn.click()
            print(" Clicked 'Add new' button successfully.")
        except Exception as e:
            print(f" Could not click 'Add new': {e}")
            return False

        try:
            self.wait.until(EC.presence_of_element_located((By.ID, "Email"))).send_keys(email)
            self.driver.find_element(By.ID, "Password").send_keys(password)
            self.driver.find_element(By.ID, "FirstName").send_keys(first_name)
            self.driver.find_element(By.ID, "LastName").send_keys(last_name)

            save_btn = self.driver.find_element(By.XPATH, "//button[@name='save']")
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", save_btn)
            time.sleep(1)
            save_btn.click()
            print(" Clicked 'Save' button.")
            return True
        except Exception as e:
            print(f" Error filling or saving form: {e}")
            return False

    def get_alert_message(self):
        try:
            time.sleep(2)
            success_alerts = self.driver.find_elements(
                By.XPATH, "//div[@class='alert alert-success alert-dismissable' and contains(.,'added successfully')]"
            )
            if success_alerts:
                print(" Detected success alert message: Customer added successfully.")
                return "success"

            duplicate_msgs = self.driver.find_elements(
                By.XPATH, "//li[contains(text(),'Email is already registered')]"
            )
            if duplicate_msgs:
                print(" Detected 'Email already registered' message.")
                return "exists"

            #  No message — take simple screenshot
            print(" No alert found ")





        except Exception as e:
            print(f" Error checking alert: {e}")
            return "none"


