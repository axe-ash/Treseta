import logging
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Base page class with common functionality for all pages"""

    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(__name__)

    def find_element(self, locator, timeout=10):
        """Find a single element with an explicit wait."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            self.logger.error(f"Element not found with locator: {locator}")
            raise

    def find_elements(self, locator, timeout=10):
        """Find multiple elements with an explicit wait."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
        except TimeoutException:
            self.logger.warning(f"No elements found with locator: {locator}")
            return []

    def click_element(self, locator, timeout=10):
        """Finds an element, waits for it to be clickable, and then clicks it."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            return element
        except TimeoutException:
            self.logger.error(f"Element with locator {locator} was not clickable.")
            raise

    def send_keys_to_element(self, locator, text, timeout=10):
        """Finds an element, clears its content, and sends keys to it."""
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)
        return element

    def get_text(self, locator, timeout=10):
        """Get text from an element."""
        element = self.find_element(locator, timeout)
        return element.text

    def is_element_visible(self, locator, timeout=10):
        """Check if an element is visible on the page."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def is_element_present(self, locator, timeout=1):
        """Check if an element is present in the DOM."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def wait_for_url_contains(self, url_part, timeout=10):
        """Wait for the URL to contain a specific text."""
        try:
            return WebDriverWait(self.driver, timeout).until(EC.url_contains(url_part))
        except TimeoutException:
            self.logger.error(f"URL did not contain '{url_part}' within {timeout}s.")
            raise

    def wait_for_page_title_contains(self, title, timeout=10):
        """Wait for the page title to contain a specific text."""
        try:
            return WebDriverWait(self.driver, timeout).until(EC.title_contains(title))
        except TimeoutException:
            self.logger.error(f"Title did not contain '{title}' within {timeout}s.")
            raise

    def scroll_to_element(self, locator, timeout=10):
        """Scroll to an element."""
        element = self.find_element(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        return element

    def get_current_url(self):
        """Get the current page URL."""
        return self.driver.current_url

    def get_page_title(self):
        """Get the page title."""
        return self.driver.title

    def take_screenshot(self, filename):
        """Take a screenshot."""
        return self.driver.save_screenshot(filename)