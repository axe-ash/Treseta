from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    """Shopping cart page object"""
    
    # Locators
    CART_TITLE = (By.CLASS_NAME, "title")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CART_ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    CART_ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "button[id*='remove']")
    CART_QUANTITY = (By.CLASS_NAME, "cart_quantity")
    
    # Dynamic locators
    CART_ITEM_BY_NAME_TEMPLATE = "//div[@class='inventory_item_name' and text()='{}']"
    REMOVE_ITEM_BUTTON_TEMPLATE = "//div[text()='{}']/ancestor::div[@class='cart_item']//button[contains(@id,'remove')]"
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://www.saucedemo.com/cart.html"
    
    def navigate_to_cart(self):
        """Navigate to cart page"""
        self.driver.get(self.url)
        return self
    
    def is_on_cart_page(self):
        """Verify if on cart page"""
        return self.is_element_visible(self.CART_TITLE) and \
               "cart.html" in self.get_current_url()
    
    def get_cart_items_count(self):
        """Get number of items in cart"""
        items = self.find_elements(self.CART_ITEMS)
        return len(items)
    
    def get_cart_item_names(self):
        """Get all product names in cart"""
        name_elements = self.find_elements(self.CART_ITEM_NAMES)
        return [element.text for element in name_elements]
    
    def get_cart_item_prices(self):
        """Get all product prices in cart"""
        price_elements = self.find_elements(self.CART_ITEM_PRICES)
        return [element.text for element in price_elements]
    
    def is_product_in_cart(self, product_name):
        """Check if specific product is in cart"""
        item_locator = (By.XPATH, self.CART_ITEM_BY_NAME_TEMPLATE.format(product_name))
        return self.is_element_visible(item_locator)
    
    def remove_product_from_cart(self, product_name):
        """Remove specific product from cart"""
        remove_button_locator = (By.XPATH, self.REMOVE_ITEM_BUTTON_TEMPLATE.format(product_name))
        self.click_element(remove_button_locator)
        return self
    
    def is_cart_empty(self):
        """Check if cart is empty"""
        return self.get_cart_items_count() == 0
    
    def proceed_to_checkout(self):
        """Click checkout button"""
        self.click_element(self.CHECKOUT_BUTTON)
        return self
    
    def continue_shopping(self):
        """Click continue shopping button"""
        self.click_element(self.CONTINUE_SHOPPING_BUTTON)
        return self
    
    def get_cart_summary(self):
        """Get cart summary with product details"""
        names = self.get_cart_item_names()
        prices = self.get_cart_item_prices()
        quantities = self.find_elements(self.CART_QUANTITY)
        
        cart_summary = []
        for i, name in enumerate(names):
            cart_summary.append({
                'name': name,
                'price': prices[i] if i < len(prices) else 'N/A',
                'quantity': quantities[i].text if i < len(quantities) else '1'
            })
        
        return cart_summary