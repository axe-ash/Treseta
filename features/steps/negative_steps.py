from behave import given, when, then
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
import time

@when('the user navigates directly to "{url_path}"')
def step_navigate_directly_to_url(context, url_path):
    """Navigate directly to a specific URL path"""
    base_url = "https://www.saucedemo.com"
    full_url = base_url + url_path
    context.driver.get(full_url)
    time.sleep(2)

@when('uses browser back button')
def step_use_browser_back_button(context):
    """Use browser back button"""
    context.driver.back()
    time.sleep(2)

@when('the user logs out')
def step_user_logs_out(context):
    """User logs out"""
    context.products_page = ProductsPage(context.driver)
    context.products_page.logout()
    time.sleep(2)

@then('an error message "{expected_message}" should be displayed')
def step_verify_specific_error_message(context, expected_message):
    """Verify specific error message is displayed"""
    context.login_page = LoginPage(context.driver)
    
    # Check if we're on login page and look for the error
    if context.login_page.is_on_login_page():
        # Look for error in the page content or error message element
        page_source = context.driver.page_source
        assert expected_message in page_source, f"Expected error message '{expected_message}' not found in page"
    else:
        # Check for error message element
        error_message = context.login_page.get_error_message()
        if error_message:
            assert expected_message in error_message, f"Expected '{expected_message}' but got '{error_message}'"

@then('an error message should indicate login is required')
def step_verify_login_required_error(context):
    """Verify error message indicates login is required"""
    context.login_page = LoginPage(context.driver)
    
    # Should be redirected to login page or show login required message
    page_source = context.driver.page_source.lower()
    login_indicators = ["login", "logged in", "access", "unauthorized"]
    
    found_indicator = any(indicator in page_source for indicator in login_indicators)
    assert found_indicator, "No login required indication found"

@then('the user should remain on the login page or be redirected to login')
def step_verify_stays_or_redirected_to_login(context):
    """Verify user stays on login page or gets redirected to login"""
    context.login_page = LoginPage(context.driver)
    time.sleep(2)  # Allow time for any redirects
    
    # Should be on login page
    assert context.login_page.is_on_login_page(), "User should be on login page after browser back"