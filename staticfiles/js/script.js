
const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
const deleteButtons = document.getElementsByClassName("btn-delete");
const deleteConfirm = document.getElementById("deleteConfirm");

function openForm() {
    document.getElementById("posting-form").style.display = "block";
    document.getElementById("posting-button").style.display = "none";
}

function closeForm() {
    document.getElementById("posting-form").style.display = "none";
    document.getElementById("posting-button").style.display = "block";
}

/**
* Initializes deletion functionality for the provided delete buttons.
* 
* For each button in the `deleteButtons` collection:
* - Retrieves the associated comment's ID upon click.
* - Updates the `deleteConfirm` link's href to point to the 
* deletion endpoint for the specific comment.
* - Displays a confirmation modal (`deleteModal`) to prompt 
* the user for confirmation before deletion.
*/
for (let button of deleteButtons) {
    button.addEventListener("click", (e) => {
      let commentId = e.target.getAttribute("comment_id");
      deleteConfirm.setAttribute("action", `/delete_comment/${commentId}`);
      deleteModal.show();
    });
  }