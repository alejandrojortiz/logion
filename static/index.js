function handleLogOutClick() {
  console.log("logout clicked");
  $.get("/logout", (response) => {
    window.location.href = response;
  });
}
