@cart
Feature: Shopping Cart Functionality
  As a logged-in user
  I want to add products to my cart
  So that I can purchase them later

  Background:
    Given the user is logged in with "standard_user" and "secret_sauce"
    And the user is on the products page

  @smoke @positive
  Scenario: Add single product to cart
    When the user adds "Sauce Labs Backpack" to cart
    Then the cart badge should display "1"
    And the cart should contain "Sauce Labs Backpack"

  @positive
  Scenario: Add multiple products to cart
    When the user adds the following products to cart:
      | Sauce Labs Backpack |
      | Sauce Labs Bike Light |
      | Sauce Labs Bolt T-Shirt |
    Then the cart badge should display "3"
    And the cart should contain all added products

  @positive
  Scenario: Remove product from cart
    Given the user has added "Sauce Labs Backpack" to cart
    When the user removes "Sauce Labs Backpack" from cart
    Then the cart badge should not be visible
    And the cart should be empty

  @positive
  Scenario: Verify product details in cart
    When the user adds "Sauce Labs Backpack" to cart
    And navigates to the cart page
    Then the cart should display:
      | Product Name        | Price  |
      | Sauce Labs Backpack | $29.99 |

  @cart_navigation
  Scenario: Continue shopping from cart
    Given the user has added "Sauce Labs Backpack" to cart
    When the user navigates to the cart page
    And clicks "Continue Shopping"
    Then the user should be on the products page