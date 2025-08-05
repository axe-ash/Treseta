from behave import given, when, then
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
import time

# Background steps
@given('the user has added the following products to cart')
def step_user_has_added_products_to_cart(context):
    """User has added multiple products to cart"""
    context.products_page = ProductsPage(context.driver)
    for row in context.table:
        product_name = row['Product Name'] if 'Product Name' in row.headings else row[0]
        context.products_page.add_product_to_cart(product_name)
        time.sleep(0.5)

# When steps
@when('the user proceeds to checkout')
def step_proceed_to_checkout(context):
    """User proceeds to checkout"""
    context.products_page = ProductsPage(context.driver)
    context.products_page.click_cart()
    
    context.cart_page = CartPage(context.driver)
    context.cart_page.proceed_to_checkout()
    
    context.checkout_page = CheckoutPage(context.driver)
    assert context.checkout_page.is_on_checkout_info_page(), "Failed to reach checkout page"

@when('enters the following checkout information')
def step_enter_checkout_information_table(context):
    """Enter checkout information from table"""
    for row in context.table:
        first_name = row['First Name']
        last_name = row['Last Name'] 
        postal_code = row['Postal Code']
        
        context.checkout_page.fill_checkout_information(first_name, last_name, postal_code)

@when('enters valid checkout information')
def step_enter_valid_checkout_info(context):
    """Enter valid checkout information"""
    context.checkout_page = CheckoutPage(context.driver)
    context.checkout_page.fill_checkout_information("John", "Doe", "12345")

@when('enters checkout information with missing "{field}"')
def step_enter_checkout_info_missing_field(context, field):
    """Enter checkout information with one field missing"""
    context.checkout_page = CheckoutPage(context.driver)
    
    first_name = "John" if field != "First Name" else ""
    last_name = "Doe" if field != "Last Name" else ""
    postal_code = "12345" if field != "Postal Code" else ""
    
    context.checkout_page.fill_checkout_information(first_name, last_name, postal_code)

@when('clicks Continue')
def step_click_continue(context):
    """Click continue button"""
    context.checkout_page.click_continue()
    time.sleep(2)

@when('clicks Cancel')
def step_click_cancel(context):
    """Click cancel button"""
    context.checkout_page.click_cancel()
    time.sleep(1)

@when('clicks Finish')
def step_click_finish(context):
    """Click finish button"""
    context.checkout_page.click_finish()
    time.sleep(2)

# Then steps
@then('the order confirmation should be displayed')
def step_verify_order_confirmation(context):
    """Verify order confirmation is displayed"""
    context.checkout_page = CheckoutPage(context.driver)
    assert context.checkout_page.is_on_checkout_complete_page(), "Order confirmation page not displayed"

@then('the confirmation message should contain "{expected_text}"')
def step_verify_confirmation_message(context, expected_text):
    """Verify confirmation message contains expected text"""
    context.checkout_page = CheckoutPage(context.driver)
    confirmation_text = context.checkout_page.get_order_complete_text()
    assert expected_text.lower() in confirmation_text.lower(), f"Confirmation text does not contain '{expected_text}'"

@then('the checkout overview should display')
def step_verify_checkout_overview_table(context):
    """Verify checkout overview displays expected items"""
    context.checkout_page = CheckoutPage(context.driver)
    summary_items = context.checkout_page.get_checkout_summary_items()
    
    for row in context.table:
        expected_item = row['Item']
        expected_quantity = row['Quantity']
        expected_price = row['Price']
        
        # Find matching item in summary
        item_found = False
        for item in summary_items:
            if item['name'] == expected_item:
                assert item['quantity'] == expected_quantity, f"Expected quantity '{expected_quantity}' but got '{item['quantity']}'"
                assert item['price'] == expected_price, f"Expected price '{expected_price}' but got '{item['price']}'"
                item_found = True
                break
        
        assert item_found, f"Item '{expected_item}' not found in checkout overview"

@then('the payment information should show "{expected_payment}"')
def step_verify_payment_info(context, expected_payment):
    """Verify payment information"""
    context.checkout_page = CheckoutPage(context.driver)
    payment_info = context.checkout_page.get_payment_information()
    assert expected_payment in payment_info, f"Expected payment info '{expected_payment}' not found in '{payment_info}'"

@then('the shipping information should show "{expected_shipping}"')
def step_verify_shipping_info(context, expected_shipping):
    """Verify shipping information"""
    context.checkout_page = CheckoutPage(context.driver)
    shipping_info = context.checkout_page.get_shipping_information()
    assert expected_shipping in shipping_info, f"Expected shipping info '{expected_shipping}' not found in '{shipping_info}'"

@then('the total should include item total and tax')
def step_verify_total_calculation(context):
    """Verify total includes item total and tax"""
    context.checkout_page = CheckoutPage(context.driver)
    
    item_total_text = context.checkout_page.get_item_total()
    tax_text = context.checkout_page.get_tax_amount()
    final_total_text = context.checkout_page.get_final_total()
    
    # Verify all totals are displayed
    assert "Item total:" in item_total_text, "Item total not displayed"
    assert "Tax:" in tax_text, "Tax amount not displayed"
    assert "Total:" in final_total_text, "Final total not displayed"

@then('an error message should be displayed for the missing "{field}"')
def step_verify_missing_field_error(context, field):
    """Verify error message for missing field"""
    context.checkout_page = CheckoutPage(context.driver)
    error_message = context.checkout_page.get_checkout_error_message()
    
    assert error_message is not None, "No error message displayed for missing field"
    
    # Check if error message mentions the missing field
    field_keywords = {
        "First Name": ["first name", "first", "name"],
        "Last Name": ["last name", "last", "name"], 
        "Postal Code": ["postal code", "postal", "zip", "code"]
    }
    
    found_keyword = False
    for keyword in field_keywords.get(field, []):
        if keyword.lower() in error_message.lower():
            found_keyword = True
            break
    
    assert found_keyword, f"Error message does not mention missing {field}: {error_message}"

@then('the user should be redirected to the cart page')
def step_verify_redirected_to_cart(context):
    """Verify user is redirected to cart page"""
    context.cart_page = CartPage(context.driver) 
    assert context.cart_page.is_on_cart_page(), "User was not redirected to cart page"