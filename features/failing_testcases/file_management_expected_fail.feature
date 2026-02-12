Feature: File Management - Expected Failures

  Scenario: TC-F1 Cross-user file access should be allowed (intentional fail)
    Given a user exists with username "victim" and password "pass"
    And I log in with username "victim" and password "pass"
    And I have uploaded a file named "secret.txt" with content "Private Data"
    And I logout

    Given a user exists with username "attacker" and password "pass"
    And I log in with username "attacker" and password "pass"
    When I attempt to download the file "secret.txt" belonging to "victim"
    Then I should receive a 200 status code
