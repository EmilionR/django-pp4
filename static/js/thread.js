const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
const deleteButtons = document.getElementsByClassName("btn-delete");
const deleteConfirm = document.getElementById("deleteConfirm");

/**
* Initializes deletion functionality for the post/comment delete buttons.
* 
* For each button in the `deleteButtons` collection:
* - Retrieve the comment ID on click.
* - Update the `deleteConfirm` link's href to point to the 
* deletion endpoint for the comment.
* - Display a modal (`deleteModal`) to prompt 
* the user for confirmation before deletion.
*/

for (let button of deleteButtons) {
  button.addEventListener("click", (e) => {
    let entryID = e.target.getAttribute("entry_id");
    let entryType = e.target.getAttribute("entry_type");
    deleteConfirm.setAttribute("action", `/delete/${entryType}/${entryID}`);
    deleteModal.show();
  });
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
 * Initializes like functionality for the like buttons.
 * Retrieves the CSRF token from the cookies and sends a POST request to the
 * like endpoint for the post.
 */
document.addEventListener('DOMContentLoaded', () => {
  let likeButtons = document.querySelectorAll('.like-btn');

  likeButtons.forEach((button) => {
    button.addEventListener('click', () => {
      let postId = button.dataset.postId;
      let contentType = button.dataset.contentType;
      let csrfToken = getCookie('csrftoken');
      // Made with help from my mentor
      fetch(`/like_${contentType}/${postId}/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          'X-CSRFToken': csrfToken
        },
      })
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json();
        })
        .then(data => {
          if (data.liked) {
            // Change icon to solid
            button.innerHTML = `<i class="fas fa-heart"></i>`;
          } else {
            // Change icon to hollow
            button.innerHTML = `<i class="far fa-heart"></i>`;
          }
          // Update the like count
          document.getElementById(`like-count-${contentType}${postId}`).textContent = data.new_likes;
        })
        .catch(error => {
          console.error("Request failed:", error);
        });
    });
  });
});
