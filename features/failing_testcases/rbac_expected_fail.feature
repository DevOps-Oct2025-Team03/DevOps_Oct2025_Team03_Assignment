Feature: RBAC - Expected Failures

  Scenario: TC-F1 Regular user should access admin dashboard (intentional fail)
    Given a user exists with username "regular" and password "user123"
    And I log in with username "regular" and password "user123"
    When I access the admin dashboard
    Then I should receive a 200 status code
