async function fetchUsers() {
    const response = await fetch('/get-users');
    const data = await response.json();

    const userList = document.getElementById('user-list');
    userList.innerHTML = ''; // Clear existing user list

    // Log data for debugging
    console.log(data);

    // Loop through users and display them
    data.forEach(user => {
        const userItem = document.createElement('div');
        userItem.classList.add('user-item');

        userItem.innerHTML = `
            <span>${user.username} - ${user.role}</span>
            <button onclick="deleteUser(${user.id})">Delete</button>
        `;

        // Append the user item to the user list container
        userList.appendChild(userItem);
    });
}




// Function to delete a user
async function deleteUser(userId) {
    const response = await fetch(`/user/delete/${userId}`, {
        method: 'DELETE',
    });

    if (response.ok) {
        alert('User deleted successfully!');
        fetchUsers(); // Refresh the list of users
    } else {
        alert('Failed to delete user.');
    }
}

// Fetch users when the page loads
window.onload = fetchUsers;
