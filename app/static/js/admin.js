// Create user
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("create-user-form");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = new FormData(form);
    const res = await fetch("/admin/create_user", { method: "POST", body: data });
    alert(res.ok ? "User created" : "Failed to create user");
    if (res.ok) window.location.reload();
  });
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
