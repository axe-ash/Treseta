"""Browser factory for WebDriver management"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from utils.config import Config
import logging

logger = logging.getLogger(__name__)

class BrowserFactory:
    """Factory class for creating WebDriver instances"""
    
    @staticmethod
    def create_driver(browser_name: str = None):
        """Create WebDriver instance based on browser name"""
        browser_name = browser_name or Config.DEFAULT_BROWSER
        browser_options = Config.get_browser_options(browser_name)
        
        logger.info(f"Creating {browser_name} driver with options: {browser_options}")
        
        if browser_name.lower() == "chrome":
            return BrowserFactory._create_chrome_driver(browser_options)
        elif browser_name.lower() == "firefox":
            return BrowserFactory._create_firefox_driver(browser_options)
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")
    
    @staticmethod
    def _create_chrome_driver(options_dict):
        """Create Chrome WebDriver"""
        chrome_options = ChromeOptions()
        
        if options_dict.get("headless", False):
            chrome_options.add_argument("--headless=new")
        
        for arg in options_dict.get("args", []):
            chrome_options.add_argument(arg)
        
        # Use WebDriverManager to handle driver installation
        service = ChromeService()
        driver = webdriver.Chrome()
        
        # Set window size
        window_size = options_dict.get("window_size", (1920, 1080))
        driver.set_window_size(*window_size)
        
        # Set timeouts
        driver.implicitly_wait(Config.IMPLICIT_WAIT)
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
        
        return driver
    
    @staticmethod
    def _create_firefox_driver(options_dict):
        """Create Firefox WebDriver"""
        firefox_options = FirefoxOptions()
        
        if options_dict.get("headless", False):
            firefox_options.add_argument("--headless")
        
        # Use WebDriverManager to handle driver installation
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=firefox_options)
        
        # Set window size
        window_size = options_dict.get("window_size", (1920, 1080))
        driver.set_window_size(*window_size)
        
        # Set timeouts
        driver.implicitly_wait(Config.IMPLICIT_WAIT)
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
        
        return driver
    
    @staticmethod
    def quit_driver(driver):
        """Safely quit WebDriver"""
        if driver:
            try:
                driver.quit()
                logger.info("WebDriver quit successfully")
            except Exception as e:
                logger.error(f"Error quitting WebDriver: {e}")