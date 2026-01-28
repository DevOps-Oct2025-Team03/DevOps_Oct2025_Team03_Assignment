Feature: Role-Based Access Control

  Scenario: TC-1 Admin Access to Admin Dashboard
    Given an admin user exists with username "admin" and password "admin123"
    And I log in with username "admin" and password "admin123"
    When I access the admin dashboard
    Then I should receive a 200 status code

  Scenario: TC-2 User Restricted from Admin Dashboard
    Given a user exists with username "regular" and password "user123"
    And I log in with username "regular" and password "user123"
    When I access the admin dashboard
    Then I should receive a 403 status code