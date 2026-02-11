document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const usernameInput = document.getElementById("username");
    const passwordInput = document.getElementById("password");

    form.addEventListener("submit", function (event) {
        let valid = true;

        // Reset previous styles
        usernameInput.style.borderColor = "#ccc";
        passwordInput.style.borderColor = "#ccc";

        // Username validation
        if (usernameInput.value.trim() === "") {
            usernameInput.style.borderColor = "red";
            valid = false;
        }

        // Password validation
        if (passwordInput.value.trim() === "") {
            passwordInput.style.borderColor = "red";
            valid = false;
        }

        // Block submission if invalid
        if (!valid) {
            event.preventDefault();
            alert("Please enter both username and password.");
        }
    });
});
