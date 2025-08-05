from behave import given, when, then
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
import time

# Background steps
@given('the user is logged in with "{username}" and "{password}"')
def step_user_logged_in(context, username, password):
    """User logs in with given credentials"""
    context.login_page = LoginPage(context.driver)
    context.login_page.navigate_to_login_page()
    context.login_page.login(username, password)
    time.sleep(2)

@given('the user is on the products page')
def step_user_on_products_page(context):
    """Verify user is on products page"""
    context.products_page = ProductsPage(context.driver)
    assert context.products_page.is_on_products_page(), "User is not on products page"

@given('the user has added "{product_name}" to cart')
def step_user_has_added_product(context, product_name):
    """User has already added a product to cart"""
    context.products_page = ProductsPage(context.driver)
    context.products_page.add_product_to_cart(product_name)
    time.sleep(1)

# When steps
@when('the user adds "{product_name}" to cart')
def step_add_product_to_cart(context, product_name):
    """Add a specific product to cart"""
    context.products_page = ProductsPage(context.driver)
    context.products_page.add_product_to_cart(product_name)
    time.sleep(1)

@when('the user adds the following products to cart')
def step_add_multiple_products_to_cart(context):
    """Add multiple products to cart"""
    context.products_page = ProductsPage(context.driver)
    for row in context.table:
        product_name = row['Product Name'] if 'Product Name' in row.headings else row[0]
        context.products_page.add_product_to_cart(product_name)
        time.sleep(0.5)

@when('the user removes "{product_name}" from cart')
def step_remove_product_from_cart(context, product_name):
    """Remove a product from cart"""
    context.products_page = ProductsPage(context.driver)
    context.products_page.remove_product_from_cart(product_name)
    time.sleep(1)

@when('navigates to the cart page')
def step_navigate_to_cart(context):
    """Navigate to cart page"""
    context.products_page = ProductsPage(context.driver)
    context.products_page.click_cart()
    context.cart_page = CartPage(context.driver)
    assert context.cart_page.is_on_cart_page(), "Failed to navigate to cart page"

@when('clicks "{button_text}"')
def step_click_button_by_text(context, button_text):
    """Click button by text"""
    context.cart_page = CartPage(context.driver)
    if button_text == "Continue Shopping":
        context.cart_page.continue_shopping()
    time.sleep(1)

# Then steps
@then('the cart badge should display "{expected_count}"')
def step_verify_cart_badge_count(context, expected_count):
    """Verify cart badge shows expected count"""
    context.products_page = ProductsPage(context.driver)
    actual_count = context.products_page.get_cart_badge_count()
    assert actual_count == expected_count, f"Expected cart badge to show '{expected_count}' but got '{actual_count}'"

@then('the cart badge should not be visible')
def step_verify_cart_badge_not_visible(context):
    """Verify cart badge is not visible"""
    context.products_page = ProductsPage(context.driver)
    assert not context.products_page.is_cart_badge_visible(), "Cart badge should not be visible"

@then('the cart should contain "{product_name}"')
def step_verify_cart_contains_product(context, product_name):
    """Verify cart contains specific product"""
    context.products_page = ProductsPage(context.driver)
    context.products_page.click_cart()
    context.cart_page = CartPage(context.driver)
    assert context.cart_page.is_product_in_cart(product_name), f"Cart does not contain '{product_name}'"

@then('the cart should contain all added products')
def step_verify_cart_contains_all_products(context):
    """Verify cart contains all products that were added"""
    context.products_page = ProductsPage(context.driver)
    context.products_page.click_cart()
    context.cart_page = CartPage(context.driver)
    
    expected_products = []
    for row in context.table:
        product_name = row['Product Name'] if 'Product Name' in row.headings else row[0]
        expected_products.append(product_name)
    
    cart_items = context.cart_page.get_cart_item_names()
    
    for product in expected_products:
        assert product in cart_items, f"Product '{product}' not found in cart"

@then('the cart should be empty')
def step_verify_cart_empty(context):
    """Verify cart is empty"""
    context.cart_page = CartPage(context.driver)
    assert context.cart_page.is_cart_empty(), "Cart is not empty"

@then('the cart should display')
def step_verify_cart_displays_table(context):
    """Verify cart displays expected product details"""
    context.cart_page = CartPage(context.driver)
    cart_summary = context.cart_page.get_cart_summary()
    
    for row in context.table:
        expected_name = row['Product Name']
        expected_price = row['Price']
        
        # Find matching product in cart
        product_found = False
        for item in cart_summary:
            if item['name'] == expected_name:
                assert item['price'] == expected_price, f"Expected price '{expected_price}' but got '{item['price']}'"
                product_found = True
                break
        
        assert product_found, f"Product '{expected_name}' not found in cart"

@then('the user should be on the products page')
def step_verify_on_products_page(context):
    """Verify user is on products page"""
    context.products_page = ProductsPage(context.driver)
    assert context.products_page.is_on_products_page(), "User is not on products page"