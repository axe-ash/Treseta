"""Behave environment setup and teardown"""
import os
import logging
from datetime import datetime
from utils.browser_factory import BrowserFactory
from utils.config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def before_all(context):
    """Setup before all tests"""
    # Create necessary directories
    os.makedirs(Config.SCREENSHOT_DIR, exist_ok=True)
    os.makedirs(Config.ALLURE_RESULTS_DIR, exist_ok=True)
    
    # Configure context
    context.config.setup_logging()
    
    # Store start time
    context.start_time = datetime.now()
    
    logging.info("Starting test execution")

def before_feature(context, feature):
    """Setup before each feature"""
    # Skip features with @skip tag
    if "skip" in feature.tags:
        feature.skip("Marked with @skip")
        return
    
    logging.info(f"Starting feature: {feature.name}")

def before_scenario(context, scenario):
    """Setup before each scenario"""
    # Skip scenarios with @skip tag
    if "skip" in scenario.effective_tags:
        scenario.skip("Marked with @skip")
        return
    
    # Get browser from command line or use default
    browser_name = context.config.userdata.get("browser", Config.DEFAULT_BROWSER)
    
    # Create WebDriver
    context.driver = BrowserFactory.create_driver(browser_name)
    
    logging.info(f"Starting scenario: {scenario.name}")

def after_scenario(context, scenario):
    """Cleanup after each scenario"""

    if hasattr(context, 'driver'):
        # Take screenshot on failure
        if scenario.status == "failed" and Config.TAKE_SCREENSHOT_ON_FAILURE:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"{scenario.name.replace(' ', '_')}_{timestamp}.png"
            screenshot_path = os.path.join(Config.SCREENSHOT_DIR, screenshot_name)

            try:
                context.driver.save_screenshot(screenshot_path)
                logging.info(f"Screenshot saved: {screenshot_path}")
            except Exception as e:
                logging.error(f"Failed to take screenshot: {e}")

        # Quit WebDriver
        BrowserFactory.quit_driver(context.driver)

    logging.info(f"Completed scenario: {scenario.name} - Status: {scenario.status}")

def after_feature(context, feature):
    """Cleanup after each feature"""
    logging.info(f"Completed feature: {feature.name}")

def after_all(context):
    """Cleanup after all tests"""
    end_time = datetime.now()
    duration = end_time - context.start_time
    
    logging.info(f"Test execution completed in {duration}")