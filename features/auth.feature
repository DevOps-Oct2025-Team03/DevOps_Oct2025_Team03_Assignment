Feature: Authentication and Authorization

  Background:
    Given the database is initialized

  Scenario: TC-1 Valid User Login
    Given a user exists with username "testuser" and password "password123"
    When I log in with username "testuser" and password "password123"
    Then I should receive a 200 status code
    And I should be logged in

  Scenario: TC-2 Invalid User Login
    Given a user exists with username "testuser" and password "password123"
    When I log in with username "testuser" and password "wrongpassword"
    Then I should receive a 401 status code
    And I should see an error message

  Scenario: TC-3 Access Control for Protected Routes
    Given I am not logged in
    When I attempt to access the dashboard
    Then I should receive a 401 status code