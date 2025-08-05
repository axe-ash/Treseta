from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ProductsPage(BasePage):
    """Products page object"""
    
    # Locators
    PRODUCTS_TITLE = (By.CLASS_NAME, "title")
    PRODUCT_SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.ID, "shopping_cart_container")
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    
    # Dynamic locators for products
    PRODUCT_NAME_TEMPLATE = "//div[@class='inventory_item_name' and text()='{}']"
    ADD_TO_CART_BUTTON_TEMPLATE = "//div[text()='{}']/ancestor::div[@class='inventory_item']//button[contains(@id,'add-to-cart')]"
    REMOVE_BUTTON_TEMPLATE = "//div[text()='{}']/ancestor::div[@class='inventory_item']//button[contains(@id,'remove')]"
    PRODUCT_PRICE_TEMPLATE = "//div[text()='{}']/ancestor::div[@class='inventory_item']//div[@class='inventory_item_price']"
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://www.saucedemo.com/inventory.html"
    
    def get_page_title_text(self):
        """Get page title text"""
        return self.get_text(self.PRODUCTS_TITLE)
    
    def is_on_products_page(self):
        """Verify if on products page"""
        return self.is_element_visible(self.PRODUCTS_TITLE) and \
               "inventory.html" in self.get_current_url()
    
    def get_cart_badge_count(self):
        """Get cart badge count"""
        if self.is_element_visible(self.CART_BADGE):
            return self.get_text(self.CART_BADGE)
        return None
    
    def is_cart_badge_visible(self):
        """Check if cart badge is visible"""
        return self.is_element_visible(self.CART_BADGE)
    
    def add_product_to_cart(self, product_name):
        """Add specific product to cart"""
        add_button_locator = (By.XPATH, self.ADD_TO_CART_BUTTON_TEMPLATE.format(product_name))
        self.click_element(add_button_locator)
        return self
    
    def remove_product_from_cart(self, product_name):
        """Remove specific product from cart"""
        remove_button_locator = (By.XPATH, self.REMOVE_BUTTON_TEMPLATE.format(product_name))
        self.click_element(remove_button_locator)
        return self
    
    def get_product_price(self, product_name):
        """Get price of specific product"""
        price_locator = (By.XPATH, self.PRODUCT_PRICE_TEMPLATE.format(product_name))
        return self.get_text(price_locator)
    
    def is_product_in_cart(self, product_name):
        """Check if product add button changed to remove"""
        remove_button_locator = (By.XPATH, self.REMOVE_BUTTON_TEMPLATE.format(product_name))
        return self.is_element_visible(remove_button_locator)
    
    def get_all_product_names(self):
        """Get all product names"""
        product_elements = self.find_elements((By.CLASS_NAME, "inventory_item_name"))
        return [element.text for element in product_elements]
    
    def click_cart(self):
        """Click cart icon"""
        self.click_element(self.CART_LINK)
        return self
    
    def open_menu(self):
        """Open hamburger menu"""
        self.click_element(self.MENU_BUTTON)
        return self
    
    def logout(self):
        """Logout from application"""
        self.open_menu()
        self.click_element(self.LOGOUT_LINK)
        return self
    
    def sort_products(self, sort_option):
        """Sort products by given option"""
        from selenium.webdriver.support.ui import Select
        dropdown = self.find_element(self.PRODUCT_SORT_DROPDOWN)
        select = Select(dropdown)
        select.select_by_visible_text(sort_option)
        return self
