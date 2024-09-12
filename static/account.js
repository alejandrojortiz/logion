// Handles a click of the logout button
function handleLogOutClick() {
  $.get("/logout", (response) => {
    window.location.href = response;
  });
}

// Handles a click of a delete button for a project row
// Removes the elements representing the prediction from the DOM
function handleDeleteClick(event) {
  console.log("DELETE CLICKED");
  const button = event.target;
  const ancestor = button.closest(".project-link-row"); // The project row container
  const textName = ancestor.querySelector(".project-link").innerText;
  const transfer = {
    text_name: textName,
  };
  request = $.post("/deleteProject", transfer, () => {
    /* NO RESPONSE HANDLING NECESSARY*/
  });
  if (ancestor) ancestor.remove();
}
