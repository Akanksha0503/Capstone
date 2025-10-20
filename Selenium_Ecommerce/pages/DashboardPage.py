import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from Selenium_Ecommerce.modules.BaseModule import BaseModule
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, \
    StaleElementReferenceException, ElementNotInteractableException


class DashboardPage(BaseModule):

    CUSTOMERS_MENU = (By.XPATH, "//a[@href='#']//p[contains(text(),'Customers')]")
    CUSTOMERS_ITEM = (By.XPATH, "//a[@href='/Admin/Customer/List']//p[contains(text(),'Customers')]")
    USER_DROPDOWN = (By.XPATH, "//a[contains(text(),'Hello')]")
    LOGOUT_LINK = (By.XPATH, "//a[@href='/logout']")
    AJAX_BUSY = (By.ID, "ajaxBusy")



    def go_to_customers(self):
        """Navigates reliably to the Customers page (works across Chrome, Edge, Firefox)."""
        print(" Navigating to Customers section...")

        try:
            # Wait until dashboard is ready
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='content-wrapper']")))

            # Wait for ajaxBusy overlay to disappear
            try:
                self.wait.until(EC.invisibility_of_element_located(self.AJAX_BUSY))
            except TimeoutException:
                print(" ajaxBusy overlay still visible — continuing anyway.")

            # --- Step 1: Click the main Customers menu (anchor, not paragraph)
            print(" Expanding Customers menu...")

            for attempt in range(3):
                try:
                    menu_link = self.driver.find_element(By.XPATH,
                                                         "//a[@href='#']//p[contains(.,'Customers')]/ancestor::a")
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", menu_link)
                    time.sleep(0.5)
                    try:
                        menu_link.click()
                    except Exception:
                        self.driver.execute_script("arguments[0].click();", menu_link)
                    print(" Main 'Customers' menu clicked.")
                    break
                except (ElementNotInteractableException, StaleElementReferenceException) as e:
                    print(f" Menu click attempt {attempt + 1} failed: {e}")
                    time.sleep(1)
            else:
                raise AssertionError("Unable to click main Customers menu.")

            # --- Step 2: Wait for submenu link to appear
            print(" Waiting for Customers submenu to appear...")
            self.wait.until(EC.presence_of_element_located(self.CUSTOMERS_ITEM))

            # --- Step 3: Click submenu safely
            for attempt in range(3):
                try:
                    submenu_link = self.driver.find_element(*self.CUSTOMERS_ITEM)
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", submenu_link)
                    time.sleep(0.5)
                    try:
                        submenu_link.click()
                    except Exception:
                        self.driver.execute_script("arguments[0].click();", submenu_link)
                    print(" Submenu 'Customers' clicked.")
                    break
                except (StaleElementReferenceException, ElementNotInteractableException) as e:
                    print(f" Submenu click retry {attempt + 1} due to: {e}")
                    time.sleep(1)
            else:
                raise AssertionError("Unable to click Customers submenu.")

            # --- Step 4: Verify Customers page is loaded
            self.wait.until(EC.visibility_of_element_located((By.ID, "SearchEmail")))
            print(" Customers page loaded successfully!")

        except Exception as e:
            print(f" Navigation to Customers failed: {e}")
            raise

    def logout(self):
        """Logs out safely, handling overlays and click interception (especially for Firefox)."""
        wait = WebDriverWait(self.driver, 15)

        print(" Preparing to log out...")

        # Wait for any ajaxBusy overlay to vanish
        try:
            wait.until(EC.invisibility_of_element_located(self.AJAX_BUSY))
        except TimeoutException:
            print(" ajaxBusy overlay did not disappear in time — continuing anyway.")

        # Locate logout link
        logout_link = wait.until(EC.presence_of_element_located(self.LOGOUT_LINK))

        # Try up to 3 times to click
        for attempt in range(3):
             try:
                # Scroll into view
                self.driver.execute_script("arguments[0].scrollIntoView(true);", logout_link)
                time.sleep(1)

                # Ensure not obscured by overlay
                try:
                    wait.until(EC.invisibility_of_element_located(self.AJAX_BUSY))
                except TimeoutException:
                    print(" Still seeing overlay — retrying click...")

                logout_link.click()
                print(" Logout clicked successfully.")
                break

             except ElementClickInterceptedException:
                print(f" Click intercepted (attempt {attempt + 1}), retrying after short wait...")
                time.sleep(2)
                if attempt == 2:
                    print(" Failed to click logout link — using JS fallback.")
                    self.driver.execute_script("arguments[0].click();", logout_link)

        # Wait for redirection to login page
        try:
            wait.until(EC.title_contains("Login"))
            print(" Logout successful — returned to login page.")
        except TimeoutException:
            print(" Logout redirection failed. Capturing screenshot for debug.")

            raise AssertionError("Logout failed — Login page not loaded after logout.")


