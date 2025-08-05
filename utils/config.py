"""Configuration management for the test suite"""
import os
from typing import Dict, Any

class Config:
    """Configuration class for test settings"""
    
    # Base URLs
    BASE_URL = "https://www.saucedemo.com/"
    
    # Browser Configuration
    DEFAULT_BROWSER = "chrome"
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    BROWSER_WIDTH = 1920
    BROWSER_HEIGHT = 1080
    
    # Timeouts
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 10
    PAGE_LOAD_TIMEOUT = 30
    
    # Test Data
    VALID_USERS = [
        "standard_user",
        "problem_user", 
        "performance_glitch_user",
        "error_user",
        "visual_user"
    ]
    
    LOCKED_USER = "locked_out_user"
    PASSWORD = "secret_sauce"
    
    # Test Configuration
    TAKE_SCREENSHOT_ON_FAILURE = True
    SCREENSHOT_DIR = "reports/screenshots"
    
    # Allure Configuration
    ALLURE_RESULTS_DIR = "reports/allure-results"
    
    @classmethod
    def get_browser_options(cls, browser_name: str) -> Dict[str, Any]:
        """Get browser-specific options"""
        if browser_name.lower() == "chrome":
            return {
                "headless": cls.HEADLESS,
                "window_size": (cls.BROWSER_WIDTH, cls.BROWSER_HEIGHT),
                "args": [
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--disable-extensions"
                ]
            }
        elif browser_name.lower() == "firefox":
            return {
                "headless": cls.HEADLESS,
                "window_size": (cls.BROWSER_WIDTH, cls.BROWSER_HEIGHT)
            }
        else:
            return {}
    
    @classmethod
    def get_environment_url(cls) -> str:
        """Get environment-specific URL"""
        env = os.getenv("TEST_ENV", "prod").lower()
        
        if env == "staging":
            return "https://staging.saucedemo.com/"
        elif env == "dev":
            return "https://dev.saucedemo.com/"
        else:
            return cls.BASE_URL