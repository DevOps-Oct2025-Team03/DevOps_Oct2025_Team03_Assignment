Feature: Authentication - Expected Failures

  Background:
    Given the database is initialized

  Scenario: TC-F1 Valid User Login should be rejected (intentional fail)
    Given a user exists with username "testuser" and password "password123"
    When I log in with username "testuser" and password "password123"
    Then I should receive a 401 status code
    And I should see an error message

  Scenario: TC-F2 Invalid User Login should succeed (intentional fail)
    Given a user exists with username "testuser" and password "password123"
    When I log in with username "testuser" and password "wrongpassword"
    Then I should receive a 200 status code
    And I should be logged in

  Scenario: TC-F3 Protected route should deny unauthenticated access (intentional fail)
    Given I am not logged in
    When I attempt to access the dashboard
    Then I should strictly receive a 403 status code
