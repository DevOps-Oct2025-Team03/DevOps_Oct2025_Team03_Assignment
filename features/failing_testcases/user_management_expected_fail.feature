Feature: Admin User Management - Expected Failures

  Background:
    Given an admin user exists with username "admin" and password "admin123"
    And I log in with username "admin" and password "admin123"

  Scenario: TC-F1 Admin creates user should not be allowed (intentional fail)
    When I create a new user with username "newuser" and password "newpass"
    Then I should strictly receive a 403 status code

  Scenario: TC-F2 Admin deletes user should not be allowed (intentional fail)
    Given a user exists with username "todelete" and password "pass"
    When I delete the user "todelete"
    Then I should strictly receive a 403 status code
