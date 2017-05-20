
Feature: User sign up
  In order to be able to use the system
  As an User
  I want to be able to sign up to the system

  # Valid scenarios

  Scenario: Clicking the get started button and the link to register displays the signup page
    When I access the URL "/"
    When I click in "GET STARTED!"
    When I click in "Does not have an account? Signup!" in modal
    Then The browser URL should be "/signup"

  Scenario: Signing up with valid information creates a new user
    When I access the URL "/"
    When I click in "GET STARTED!"
    When I click in "Does not have an account? Signup!" in modal
    Then The browser URL should be "/signup"
    When I fill "notificaruser" in "username" field in modal
    When I fill "userpass" in "password" field in modal
    When I click in "signup_btn" button
    Then The browser URL should be "/login"
    Then The user "notificaruser" should be registered
    Then I should see "Registered with success!" in page