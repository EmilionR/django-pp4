function editAbout() {
    document.getElementById("about").style.display = "none";
    document.getElementById("edit-about").style.display = "block";
}

function cancelEdit() {
    document.getElementById("edit-about").style.display = "none";
    document.getElementById("about").style.display = "block";
}

// Retrieve the CSRF token from the cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Initializes deletion functionality for the profile delete button.
* 
* - On the `deleteConfirm` button:
* - Retrieve the profile ID on click.
* - Update the `confirmDelete` link's href to point to the 
* deletion endpoint for the profile.
* - Display a modal (`deleteModal`) to prompt 
* the user for confirmation before deletion.
 */
document.getElementById('confirmDelete').addEventListener('click', function () {
    // Retrieve the CSRF token
    let csrfToken = getCookie('csrftoken');
    // Send AJAX request to the delete account view
    fetch('/user_profile/delete_account/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
    })
        .then(response => {
            if (response.ok) {
                // Redirect to home page
                window.location.href = '/';
            } else {
                // Handle bad responses
                console.error('Failed to delete account');
            }
        })
        .catch(error => {
            // Handle network error
            console.error('Network error:', error);
        });
});