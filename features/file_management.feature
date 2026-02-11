Feature: File Management and Security

  Scenario: TC-1 User Uploads File
    Given a user exists with username "uploader" and password "pass"
    And I log in with username "uploader" and password "pass"
    When I upload a file named "my_document.txt"
    Then I should receive a 200 status code
    And the file "my_document.txt" should exist

  Scenario: TC-2 User Downloads Own File
    Given a user exists with username "downloader" and password "pass"
    And I log in with username "downloader" and password "pass"
    And I have uploaded a file named "download_me.txt"
    When I download the file "download_me.txt"
    Then I should receive a 200 status code

  Scenario: TC-3 User Deletes Own File
    Given a user exists with username "deleter" and password "pass"
    And I log in with username "deleter" and password "pass"
    And I have uploaded a file named "delete_me.txt"
    When I delete the file "delete_me.txt"
    Then I should receive a 200 status code

  Scenario: TC-4 Prevent Cross-User File Access
    # Setup: User A creates a file
    Given a user exists with username "victim" and password "pass"
    And I log in with username "victim" and password "pass"
    And I have uploaded a file named "secret.txt" with content "Private Data"
    And I logout
    
    # Action: User B tries to access it
    Given a user exists with username "attacker" and password "pass"
    And I log in with username "attacker" and password "pass"
    When I attempt to download the file "secret.txt" belonging to "victim"
    Then I should receive a 403 status code