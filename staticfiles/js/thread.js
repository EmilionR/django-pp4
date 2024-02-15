const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
const deleteButtons = document.getElementsByClassName("btn-delete");
const deleteConfirm = document.getElementById("deleteConfirm");

/**
* Initializes deletion functionality for the provided delete buttons.
* 
* For each button in the `deleteButtons` collection:
* - Retrieves the comment's ID on click.
* - Updates the `deleteConfirm` link's href to point to the 
* deletion endpoint for the comment.
* - Displays a modal (`deleteModal`) to prompt 
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

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i =  0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length +  1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length +  1));
              break;
          }
      }
  }
  return cookieValue;
}

document.addEventListener('DOMContentLoaded', () => {
  let likeButtons = document.querySelectorAll('.like-btn');

  likeButtons.forEach((button) => {
    button.addEventListener('click', () => {
      let postId = button.dataset.postId;
      let csrfToken = getCookie('csrftoken');
      console.log("Ajax, Post ID:", postId);

      fetch(`/post/${postId}/like/`, {
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
          button.innerHTML = `<i class="fas fa-heart"></i>`;
          // Update any other UI elements here
        } else {
          button.textContent = `<i class="fas fa-heart"></i>`;
          // Update any other UI elements here
        }
      })
      .catch(error => {
        console.error("Request failed:", error);
      });
    });
  });
});
