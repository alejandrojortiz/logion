function handleLogOutClick() {
  $.get("/logout", (response) => {
    window.location.href = response;
  });
}
