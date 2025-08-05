@negative
Feature: Negative Test Scenarios
  To ensure application robustness
  I want to test edge cases and error conditions

  @error_handling
  Scenario: Direct URL access without login
    When the user navigates directly to "/inventory.html"
    Then the user should be redirected to the login page
    And an error message "You can only access '/inventory.html' when you are logged in." should be displayed

  @error_handling
  Scenario: Cart access without login
    When the user navigates directly to "/cart.html"
    Then the user should be redirected to the login page
    And an error message should indicate login is required

  @data_validation
  Scenario: XSS attempt in login fields
    Given the user is on the login page
    When the user enters "<script>alert('xss')</script>" and "secret_sauce"
    And clicks the login button
    Then the login should fail with appropriate error handling

  @browser_back
  Scenario: Browser back button after logout
    Given the user logs in with "standard_user" and "secret_sauce"
    When the user logs out
    And uses browser back button
    Then the user should remain on the login page or be redirected to login