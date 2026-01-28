Feature: Admin User Management

  Background:
    Given an admin user exists with username "admin" and password "adminpass"
    And I log in with username "admin" and password "adminpass"

  Scenario: TC-1 Admin Creates User
    When I create a new user with username "newuser" and password "newpass"
    Then I should receive a 201 status code
    And the user "newuser" should exist in the system

  Scenario: TC-2 Admin Deletes User
    Given a user exists with username "todelete" and password "pass"
    When I delete the user "todelete"
    Then I should receive a 200 status code
    And the user "todelete" should not exist in the system