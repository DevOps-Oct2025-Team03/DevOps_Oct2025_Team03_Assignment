// Create user
document.getElementById("create-user-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const form = e.target;
    const data = new FormData(form);

    const res = await fetch("/admin/create_user", {
        method: "POST",
        body: data
    });

    if (res.ok) {
        alert("User created");
        window.location.reload();
    } else {
        alert("Failed to create user");
    }
});

// Delete user
async function deleteUser(userId) {
    if (!confirm("Are you sure you want to delete this user?")) return;

    const res = await fetch(`/admin/delete_user/${userId}`, {
        method: "POST"
    });

    if (res.ok) {
        alert("User deleted");
        window.location.reload();
    } else {
        alert("Failed to delete user");
    }
}
