@checkout
Feature: Checkout Process
  As a user with items in cart
  I want to complete the checkout process
  So that I can purchase the products

  Background:
    Given the user is logged in with "standard_user" and "secret_sauce"
    And the user has added the following products to cart:
      | Sauce Labs Backpack |
      | Sauce Labs Bike Light |

  @smoke @positive
  Scenario: Complete checkout with valid information
    When the user proceeds to checkout
    And enters the following checkout information:
      | First Name | Last Name | Postal Code |
      | John       | Doe       | 12345       |
    And clicks Continue
    And clicks Finish
    Then the order confirmation should be displayed
    And the confirmation message should contain "Thank you for your order!"

  @positive
  Scenario: Checkout overview verification
    When the user proceeds to checkout
    And enters valid checkout information
    And clicks Continue
    Then the checkout overview should display:
      | Item                  | Quantity | Price  |
      | Sauce Labs Backpack   | 1        | $29.99 |
      | Sauce Labs Bike Light | 1        | $9.99  |
    And the payment information should show "SauceCard #31337"
    And the shipping information should show "Free Pony Express Delivery!"
    And the total should include item total and tax

  @negative
  Scenario Outline: Checkout fails with missing information
    When the user proceeds to checkout
    And enters checkout information with missing "<field>"
    And clicks Continue
    Then an error message should be displayed for the missing "<field>"

    Examples:
      | field       |
      | First Name  |
      | Last Name   |
      | Postal Code |

  @checkout_navigation
  Scenario: Cancel checkout process
    When the user proceeds to checkout
    And clicks Cancel
    Then the user should be redirected to the cart page