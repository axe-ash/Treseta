from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CheckoutPage(BasePage):
    """Checkout page objects for all checkout steps"""
    
    # Step One - Information
    FIRST_NAME_FIELD = (By.ID, "first-name")
    LAST_NAME_FIELD = (By.ID, "last-name")
    POSTAL_CODE_FIELD = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    
    # Step Two - Overview
    CHECKOUT_SUMMARY_ITEMS = (By.CLASS_NAME, "cart_item")
    CHECKOUT_ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    CHECKOUT_ITEM_QUANTITIES = (By.CLASS_NAME, "cart_quantity")
    PAYMENT_INFO = (By.CSS_SELECTOR, "[data-test='payment-info-value']")
    SHIPPING_INFO = (By.CSS_SELECTOR, "[data-test='shipping-info-value']")
    ITEM_TOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX_TOTAL = (By.CLASS_NAME, "summary_tax_label")
    FINAL_TOTAL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")
    
    # Complete Page
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    COMPLETE_TEXT = (By.CLASS_NAME, "complete-text")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.info_url = "https://www.saucedemo.com/checkout-step-one.html"
        self.overview_url = "https://www.saucedemo.com/checkout-step-two.html"
        self.complete_url = "https://www.saucedemo.com/checkout-complete.html"
    
    # Step One Methods
    def enter_first_name(self, first_name):
        """Enter first name"""
        self.send_keys_to_element(self.FIRST_NAME_FIELD, first_name)
        return self
    
    def enter_last_name(self, last_name):
        """Enter last name"""
        self.send_keys_to_element(self.LAST_NAME_FIELD, last_name)
        return self
    
    def enter_postal_code(self, postal_code):
        """Enter postal code"""
        self.send_keys_to_element(self.POSTAL_CODE_FIELD, postal_code)
        return self
    
    def fill_checkout_information(self, first_name, last_name, postal_code):
        """Fill all checkout information"""
        if first_name:
            self.enter_first_name(first_name)
        if last_name:
            self.enter_last_name(last_name)
        if postal_code:
            self.enter_postal_code(postal_code)
        return self
    
    def click_continue(self):
        """Click continue button"""
        self.click_element(self.CONTINUE_BUTTON)
        return self
    
    def click_cancel(self):
        """Click cancel button"""
        self.click_element(self.CANCEL_BUTTON)
        return self
    
    def get_checkout_error_message(self):
        """Get checkout error message"""
        if self.is_element_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return None
    
    def is_on_checkout_info_page(self):
        """Verify if on checkout information page"""
        return "checkout-step-one.html" in self.get_current_url()
    
    # Step Two Methods
    def get_payment_information(self):
        """Get payment information"""
        return self.get_text(self.PAYMENT_INFO)
    
    def get_shipping_information(self):
        """Get shipping information"""
        return self.get_text(self.SHIPPING_INFO)
    
    def get_item_total(self):
        """Get item total amount"""
        return self.get_text(self.ITEM_TOTAL)
    
    def get_tax_amount(self):
        """Get tax amount"""
        return self.get_text(self.TAX_TOTAL)
    
    def get_final_total(self):
        """Get final total amount"""
        return self.get_text(self.FINAL_TOTAL)
    
    def get_checkout_summary_items(self):
        """Get all items in the checkout summary."""
        # Ensure items are loaded before fetching details
        self.find_elements(self.CHECKOUT_SUMMARY_ITEMS)

        names = [el.text for el in self.find_elements(self.CHECKOUT_ITEM_NAMES)]
        prices = [el.text for el in self.find_elements(self.CHECKOUT_ITEM_PRICES)]
        quantities = [el.text for el in self.find_elements(self.CHECKOUT_ITEM_QUANTITIES)]

        summary_items = []
        for i, name in enumerate(names):
            summary_items.append({
                'name': name,
                'price': prices[i] if i < len(prices) else 'N/A',
                'quantity': quantities[i] if i < len(quantities) else 'N/A',
            })

        return summary_items
    
    def click_finish(self):
        """Click finish button"""
        self.click_element(self.FINISH_BUTTON)
        return self
    
    def is_on_checkout_overview_page(self):
        """Verify if on checkout overview page"""
        return "checkout-step-two.html" in self.get_current_url()
    
    # Complete Page Methods
    def get_order_complete_header(self):
        """Get order complete header text"""
        return self.get_text(self.COMPLETE_HEADER)
    
    def get_order_complete_text(self):
        """Get order complete description text"""
        return self.get_text(self.COMPLETE_TEXT)
    
    def click_back_home(self):
        """Click back to products button"""
        self.click_element(self.BACK_HOME_BUTTON)
        return self
    
    def is_on_checkout_complete_page(self):
        """Verify if on checkout complete page"""
        return "checkout-complete.html" in self.get_current_url()
    
    def is_order_completed(self):
        """Verify if order is completed successfully"""
        return self.is_on_checkout_complete_page() and \
               self.is_element_visible(self.COMPLETE_HEADER)