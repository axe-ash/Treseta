from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    """Login page object"""
    
    # Locators
    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    ERROR_BUTTON = (By.CSS_SELECTOR, ".error-button")
    ACCEPTED_USERNAMES = (By.CSS_SELECTOR, "#login_credentials")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://www.saucedemo.com/"
    
    def navigate_to_login_page(self):
        """Navigate to login page"""
        self.driver.get(self.url)
        return self
    
    def enter_username(self, username):
        """Enter username"""
        self.send_keys_to_element(self.USERNAME_FIELD, username)
        return self
    
    def enter_password(self, password):
        """Enter password"""
        self.send_keys_to_element(self.PASSWORD_FIELD, password)
        return self
    
    def click_login_button(self):
        """Click login button"""
        self.click_element(self.LOGIN_BUTTON)
        return self
    
    def login(self, username, password):
        """Complete login process"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        return self
    
    def get_error_message(self):
        """Get error message text"""
        if self.is_element_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return None
    
    def is_error_displayed(self):
        """Check if error message is displayed"""
        return self.is_element_visible(self.ERROR_MESSAGE)
    
    def clear_error_message(self):
        """Clear error message by clicking X button"""
        if self.is_element_visible(self.ERROR_BUTTON):
            self.click_element(self.ERROR_BUTTON)
        return self
    
    def get_accepted_usernames(self):
        """Get list of accepted usernames"""
        if self.is_element_visible(self.ACCEPTED_USERNAMES):
            text = self.get_text(self.ACCEPTED_USERNAMES)
            # Extract usernames from the text
            usernames = []
            lines = text.split('\n')
            for line in lines:
                if line.strip() and not line.startswith('Accepted'):
                    usernames.append(line.strip())
            return usernames
        return []
    
    def is_on_login_page(self):
        """Verify if on login page"""
        return self.is_element_visible(self.LOGIN_BUTTON) and \
               "saucedemo.com" in self.get_current_url()