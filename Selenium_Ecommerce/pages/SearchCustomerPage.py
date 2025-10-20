

from selenium.common import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Selenium_Ecommerce.modules.BaseModule import BaseModule

class SearchCustomerPage(BaseModule):
    SEARCH_EMAIL = (By.ID, "SearchEmail")
    SEARCH_FIRST_NAME = (By.ID, "SearchFirstName")
    SEARCH_LAST_NAME = (By.ID, "SearchLastName")
    SEARCH_BUTTON = (By.ID, "search-customers")
    SEARCH_RESULTS = (By.XPATH, "//table[@id='customers-grid']/tbody/tr")
    PAGE_HEADER = (By.XPATH, "//h1[contains(text(),'Customers')]")

    ROLE_DROPDOWN_INPUT = (By.CSS_SELECTOR, "span.select2-selection__rendered input.select2-search__field")

    def __init__(self, driver):
        super().__init__(driver)

    def wait_for_customer_page(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.PAGE_HEADER)
        )

    def search_by_email(self, email):
        self.enter_text(*self.SEARCH_EMAIL, email)
        self.click_element(*self.SEARCH_BUTTON)
        return len(self.driver.find_elements(*self.SEARCH_RESULTS)) > 0

    def search_by_first_name(self, first_name):
        self.enter_text(*self.SEARCH_FIRST_NAME, first_name)
        self.click_element(*self.SEARCH_BUTTON)
        return len(self.driver.find_elements(*self.SEARCH_RESULTS)) > 0

    def search_by_last_name(self, last_name):
        self.enter_text(*self.SEARCH_LAST_NAME, last_name)
        self.click_element(*self.SEARCH_BUTTON)
        return len(self.driver.find_elements(*self.SEARCH_RESULTS)) > 0


    def search_by_role(self, role_name: str) -> bool:
        wait = WebDriverWait(self.driver, 10)

        # Retry loop to handle stale elements
        for _ in range(3):
            try:
                # 1️⃣ Click the Select2 container to open the dropdown
                dropdown_container = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "span.select2-selection.select2-selection--multiple"))
                )
                dropdown_container.click()

                # 2️⃣ Wait for the input field inside dropdown
                dropdown_input = wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "input.select2-search__field"))
                )
                dropdown_input.clear()
                dropdown_input.send_keys(role_name)

                # 3️⃣ Wait for the option to appear and click it
                role_option = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH,
                         f"//li[contains(@class,'select2-results__option') and normalize-space(text())='{role_name}']")
                    )
                )
                role_option.click()

                # 4️⃣ Click the search button
                search_button = wait.until(
                    EC.element_to_be_clickable(self.SEARCH_BUTTON)
                )
                search_button.click()

                # 5️⃣ Return True if search results exist
                return len(self.driver.find_elements(*self.SEARCH_RESULTS)) > 0

            except StaleElementReferenceException:
                # Element went stale — retry
                continue
            except TimeoutException:
                # Element never appeared — fail immediately
                raise

        # If all retries failed
        raise StaleElementReferenceException(f"Failed to select role '{role_name}' due to stale elements.")