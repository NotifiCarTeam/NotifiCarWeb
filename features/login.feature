
Feature: User sign in
  In order to be able to access the system funcionalities
  As an User
  I want to be able to login into the system

  # Valid scenarios

  Scenario: Clicking the get started button displays the login page
    When I access the URL "/"
    When I click in "GET STARTED!"
    Then The browser URL should be "/login"

  Scenario: Logging in with a valid user
    Given The user "notificaruser" with the password "userpass"
    When I access the URL "/"
    When I click in "GET STARTED!"
    Then The browser URL should be "/login"
    When I fill "notificaruser" in "username" field in modal
    When I fill "userpass" in "password" field in modal
    When I click in "login_btn" button
    Then The browser URL should be "/car/"
    Then I should see "Hello, notificaruser!" in "username_tag"

  # Invalid scenarios

  Scenario: Logging in with an unregistered user
    When I access the URL "/"
    When I click in "GET STARTED!"
    Then The browser URL should be "/login"
    When I fill "notregistered" in "username" field in modal
    When I fill "fakepass" in "password" field in modal
    When I click in "login_btn" button
    Then The browser URL should be "/login"
    Then I should see "Please enter a correct username and password" in page

  Scenario: Logging in without username and password
    When I access the URL "/"
    When I click in "GET STARTED!"
    Then The browser URL should be "/login"
    When I click in "login_btn" button in modal
    Then The browser URL should be "/login"
    Then The field "id_username" should have an error
    Then The field "id_password" should have an error

  Scenario: Logging in without username
    When I access the URL "/"
    When I click in "GET STARTED!"
    Then The browser URL should be "/login"
    When I fill "pass" in "password" field in modal
    When I click in "login_btn" button
    Then The browser URL should be "/login"
    Then The field "id_username" should have an error

  Scenario: Logging in without password
    When I access the URL "/"
    When I click in "GET STARTED!"
    Then The browser URL should be "/login"
    When I fill "notificaruser" in "username" field in modal
    When I click in "login_btn" button
    Then The browser URL should be "/login"
    Then The field "id_password" should have an error
