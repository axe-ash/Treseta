@login
Feature: User Login
  As a user of SauceDemo
  I want to login to the application
  So that I can access the product catalog

  Background:
    Given the user navigates to the SauceDemo login page

  @smoke @positive
  Scenario: Successful login with valid credentials
    When the user enters "standard_user" and "secret_sauce"
    And clicks the login button
    Then the user should be redirected to the products page
    And the page title should contain "Products"

  @positive
  Scenario Outline: Successful login with different valid users
    When the user enters "<username>" and "secret_sauce"
    And clicks the login button
    Then the user should be redirected to the products page

    Examples:
      | username              |
      | standard_user         |
      | problem_user          |
      | performance_glitch_user |
      | error_user            |
      | visual_user           |

  @negative
  Scenario: Login failure with locked out user
    When the user enters "locked_out_user" and "secret_sauce"
    And clicks the login button
    Then an error message "Sorry, this user has been locked out." should be displayed
    And the user should remain on the login page

  @negative
  Scenario Outline: Login failure with invalid credentials
    When the user enters "<username>" and "<password>"
    And clicks the login button
    Then an error message containing "Username and password do not match" should be displayed

    Examples:
      | username     | password      |
      | invalid_user | secret_sauce  |
      | standard_user| wrong_password|
      |              | secret_sauce  |
      | standard_user|               |

  @logout
  Scenario: User logout functionality
    Given the user logs in with "standard_user" and "secret_sauce"
    When the user clicks on the menu button
    And clicks on the logout link
    Then the user should be redirected to the login page