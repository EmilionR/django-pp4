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