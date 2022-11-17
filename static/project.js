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
function handlePredictResponse(response) {
  console.log("PREDICTED");
  $("#prediction-output").html(response);
}
function handleSaveProjectResponse(response) {
  notyf = new Notyf();
  notyf.success("Project Saved");
  console.log("Project Saved");
}
function handleSavePredictionResponse(response) {
  notyf = new Notyf();
  notyf.success("Prediction Saved!");
  console.log("Prediction Saved");
}
function handleSavePredictionClick() {
  return;
  predictionName = $("#prediction-name-input").val();
  tokenNum = $("#token-number").val();
  prediction = "";
  textID = "";
  trasnfer = {
    token_number: tokenNum,
    prediction: prediction,
    prediction_name: predictionName,
    text_id: textID,
  };
  request = $.post("/savePrediction", transfer, handleSavePredictionResponse);
}
function handleSaveProjectClick() {
  textName = $("#project-name-input").val();
  text = $("#editor").val();
  userID = window.location.pathname.split("/");
  userID = userID[2];
  transfer = {
    user_id: userID,
    text: text,
    text_name: textName,
  };
  request = $.post("/saveProject", transfer, handleSaveProjectResponse);
}
function handlePredictClick() {
  console.log("Clicked");
  const text = getHighlight();
  if (!text) return;
  transfer = {
    text: text,
    numTokens: $("#token-number").val(),
  };
  request = $.post("/predict", transfer, handlePredictResponse);
}
function handleDeleteClick(event) {
  // console.log("DELETE CLICKED");
  const button = event.target;
  const ancestor = button.closest(".single-prediction-container");
  if (ancestor) ancestor.remove();
}
function getPageState(event) {
  const button = event.target;
  const ancestor = button.closest(".single-prediction-container");
  const prediction = ancestor.querySelector('.prediction-text-container');
  let obj = {
    text: $('#editor').val(),
    numTokens: $('#token-number').val(),
    prediction: prediction,
    prefix: "",
    suffix: "",
    distance: "",
    highlightStart: $('#editor').prop('predictionStart'),
    highlightEnd: $('#editor').prop('predictionEnd')
  }
}