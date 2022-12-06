/*
Functions and event handlers to provide the client side functionality
for a project page.
*/

/* 
Generic debounce function
Used in the selectionchange event listener to limit the number of 
selectionchange events that trigger a highlight capture 
*/
function debounce(fn, delay) {
  let timer = null;
  return function () {
    var context = this,
      args = arguments;
    clearTimeout(timer);
    timer = setTimeout(function () {
      fn.apply(context, args);
    }, delay);
  };
}
const DEBOUNCE_DURATION = 100;
document.addEventListener(
  "selectionchange",
  debounce(getHighlight, DEBOUNCE_DURATION)
);

// Gets the highlighted text in the textarea element with id=editor
function getHighlight() {
  // Get text
  const editor = $("#editor");
  let text = editor.val();
  if (!text) return "";
  if (editor.prop("selectionStart") == editor.prop("selectionEnd")) return "";

  // Replace selection with the appropriate number of tokens
  const numTokens = $("#token-number").val();
  let ret = text.substring(0, editor.prop("selectionStart"));
  for (let i = 0; i < numTokens; i++) {
    if (i == 0) ret += " {tok.mask_token} ";
    else ret += "{tok.mask_token} ";
  }
  ret += text.substring(editor.prop("selectionEnd"));
  return ret;
}

// Handles the response from saving a prediction
function handleSavePredictionResponse(response) {
  notyf = new Notyf();
  notyf.success("Prediction Saved!");
  console.log("Prediction Saved");
  $("#prev-predictions-container").html(response);
}

// Handles a click on a save prediction button
function handleSavePredictionClick(event) {
  const button = event.target;
  const ancestor = button.closest(".single-prediction-container");
  const prediction = ancestor.querySelector(
    ".prediction-text-container"
  ).innerText;
  console.log("CLICKED PREDICTION SAVE");
  const predictionName = prompt("Enter prediction name");
  if (!predictionName) return; // Client must enter a name to save a prediction

  // Get prediction info
  const tokenNum = $("#token-number").val();
  const time = new Date().toLocaleDateString();
  let textID = window.location.pathname.split("/");
  textID = textID[3];

  // Get page state

  // Save prediction
  const transfer = {
    token_number: tokenNum,
    prediction: prediction,
    prediction_name: predictionName,
    text_id: textID,
    save_time: time,
    prediction_blob: "TEST",
  };
  console.log("TRANSFER", transfer);
  request = $.post("/savePrediction", transfer, handleSavePredictionResponse);
}

// Handles the response from saving a project
function handleSaveProjectResponse(response) {
  notyf = new Notyf();
  notyf.success("Project Saved");
  console.log("Project Saved");
}

// Handles a click of the save project button
function handleSaveProjectClick() {
  // console.log($("#text-name").prop("innerText"));

  // Check if there is already a text name (true for projects that have
  // already been saved) or prompt user to enter one if not
  if ($("#text-name").prop("innerText")) {
    textName = $("#text-name").prop("innerText");
  } else {
    textName = prompt("Enter text name");
  }
  if (!textName) return; // User must enter a text name to save a project

  // Get text content of the textarea
  text = $("#editor").val();
  if (text == "") {
    let notyf = new Notyf();
    notyf.error("Can't save empty text");
    return;
  }

  // Get user id
  userID = window.location.pathname.split("/");
  userID = userID[2];

  // Send data to server
  transfer = {
    user_id: userID,
    text: text,
    text_name: textName,
    time: new Date().toLocaleString(),
  };
  request = $.post("/saveProject", transfer, handleSaveProjectResponse);
}

// Handles the response from generating a model prediction
function handlePredictResponse(response) {
  console.log("PREDICTED");
  $("#prediction-output").html(response);
}

// Handles a click of the prediction button
function handlePredictClick() {
  console.log("Clicked");
  const text = getHighlight();
  if (!text) return;
  transfer = {
    text: text,
    numTokens: $("#token-number").val(),
  };
  request = $.post("/predict", transfer, handlePredictResponse);
  document.getElementById("editor").focus();
}

// Handles a click of a delete button for a prediction
// Removes the elements representing the prediction from the DOM
function handleDeleteClick(event) {
  // console.log("DELETE CLICKED");
  const button = event.target;
  const ancestor = button.closest(".single-prediction-container");
  if (ancestor) ancestor.remove();
}

// Called when a save prediction button is clicked
// Gets the page state and information about the prediction
function getPageState(event) {
  const button = event.target;
  const ancestor = button.closest(".single-prediction-container");
  const prediction = ancestor.querySelector(".prediction-text-container");
  let obj = {
    text: $("#editor").val(),
    numTokens: $("#token-number").val(),
    prediction: prediction,
    prefix: "",
    suffix: "",
    distance: "",
    highlightStart: $("#editor").prop("predictionStart"),
    highlightEnd: $("#editor").prop("predictionEnd"),
  };
}
