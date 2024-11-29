async function fetchUsers() {
    try {
        const response = await fetch('/get-users');
        if (!response.ok) {
            throw new Error(`Error: ${response.status} - ${response.statusText}`);
        }

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
                <span>${user.username}</span>
                <select class="role-dropdown" onchange="changeUserRole(${user.id}, this.value)">
                    <option value="USER" ${user.role === 'USER' ? 'selected' : ''}>USER</option>
                    <option value="ADMIN" ${user.role === 'ADMIN' ? 'selected' : ''}>ADMIN</option>
                </select>
                <button onclick="deleteUser(${user.id})">Delete</button>
            `;

            // Append the user item to the user list container
            userList.appendChild(userItem);
        });
    } catch (error) {
        console.error('Failed to fetch users:', error);
        const userList = document.getElementById('user-list');
        userList.innerHTML = `<div class="error-message">Failed to load users. Please try again later.</div>`;
    }
}

// Example function to handle role change
function changeUserRole(userId, newRole) {
    console.log(`User ID: ${userId}, New Role: ${newRole}`);
    // Send the updated role to the server if needed
    fetch(`/user/update/${userId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ role: newRole }),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to update role');
            }
            console.log(response.json);
            console.log(`Role updated successfully for user ID: ${userId}`);
        })
        .catch(error => console.error('Error updating role:', error));
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
