from behave import given, when, then
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
import time

@given('the user navigates to the SauceDemo login page')
def step_navigate_to_login_page(context):
    """Navigate to the SauceDemo login page"""
    context.login_page = LoginPage(context.driver)
    context.login_page.navigate_to_login_page()

@given('the user is on the login page')
def step_user_on_login_page(context):
    """Verify user is on login page"""
    context.login_page = LoginPage(context.driver)
    assert context.login_page.is_on_login_page(), "User is not on login page"

@given('the user logs in with "{username}" and "{password}"')
def step_user_logs_in(context, username, password):
    """User logs in with credentials"""
    context.login_page = LoginPage(context.driver)
    context.login_page.navigate_to_login_page()
    context.login_page.login(username, password)
    # Wait for navigation
    time.sleep(2)

@when('the user enters "{username}" and "{password}"')
def step_enter_credentials(context, username, password):
    """Enter username and password"""
    if not hasattr(context, 'login_page'):
        context.login_page = LoginPage(context.driver)
    
    if username:
        context.login_page.enter_username(username)
    if password:
        context.login_page.enter_password(password)

@when('clicks the login button')
def step_click_login_button(context):
    """Click the login button"""
    context.login_page.click_login_button()
    # Wait for potential navigation or error
    time.sleep(2)

@when('the user clicks on the menu button')
def step_click_menu_button(context):
    """Click hamburger menu button"""
    context.products_page = ProductsPage(context.driver)
    context.products_page.open_menu()

@when('clicks on the logout link')
def step_click_logout_link(context):
    """Click logout link"""
    context.products_page.click_element(context.products_page.LOGOUT_LINK)

@then('the user should be redirected to the products page')
def step_verify_products_page(context):
    """Verify user is on products page"""
    context.products_page = ProductsPage(context.driver)
    assert context.products_page.is_on_products_page(), "User was not redirected to products page"

@then('the page title should contain "{expected_text}"')
def step_verify_page_title_contains(context, expected_text):
    """Verify page title contains expected text"""
    context.products_page = ProductsPage(context.driver)
    page_title = context.products_page.get_page_title_text()
    assert expected_text in page_title, f"Page title '{page_title}' does not contain '{expected_text}'"

@then('a login error message "{expected_message}" should be displayed')
def step_verify_exact_error_message(context, expected_message):
    """Verify exact error message is displayed"""
    error_message = context.login_page.get_error_message()
    assert error_message is not None, "No error message was displayed"
    assert expected_message in error_message, f"Expected '{expected_message}' but got '{error_message}'"

@then('an error message containing "{expected_text}" should be displayed')
def step_verify_error_message_contains(context, expected_text):
    """Verify error message contains expected text"""
    error_message = context.login_page.get_error_message()
    assert error_message is not None, "No error message was displayed"
    assert expected_text.lower() in error_message.lower(), f"Error message '{error_message}' does not contain '{expected_text}'"

@then('the user should remain on the login page')
def step_verify_still_on_login_page(context):
    """Verify user is still on login page"""
    assert context.login_page.is_on_login_page(), "User is not on login page"

@then('the user should be redirected to the login page')
def step_verify_redirected_to_login_page(context):
    """Verify user is redirected to login page"""
    context.login_page = LoginPage(context.driver)
    time.sleep(2)  # Wait for potential redirect
    assert context.login_page.is_on_login_page(), "User was not redirected to login page"

@then('the login should fail with appropriate error handling')
def step_verify_login_fails_with_error_handling(context):
    """Verify login fails and proper error handling occurs"""
    # Should either show an error message or remain on login page
    is_on_login = context.login_page.is_on_login_page()
    has_error = context.login_page.is_error_displayed()
    
    assert is_on_login or has_error, "Login should fail with either error message or staying on login page"