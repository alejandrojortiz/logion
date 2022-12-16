/*
Functions and event handlers to provide the client side functionality
for a project page.

Author: Alejandro Ortiz
*/

//----------------------------------------------------------------------

let textArea = document.getElementById("editor");
let textDiv = null;

// Gets the highlighted text in the textarea element with id=editor
function getHighlight() {
  // Get text
  const editor = $("#editor");
  let text = editor.val();
  if (!text) return ""; // Must have text to highlight
  // Must have distinct selection
  if (editor.prop("selectionStart") == editor.prop("selectionEnd")) return "";

  let numTokens = $("#token-number").val();
  // Validate token-number input
  numTokens = Number(numTokens);
  if (!numTokens) {
    let notyf = new Notyf();
    notyf.error("Token number input must be numeric");
    return "";
  }
  if (numTokens <= 0) {
    let notyf = new Notyf();
    notyf.error("Token number must be greater than 0");
    return "";
  }
  // Get the text up to the start of the selection
  let ret = text.substring(0, editor.prop("selectionStart"));
  let styledText = ret;
  // Replace selection with the appropriate number of tokens
  for (let i = 0; i < numTokens; i++) {
    if (i == 0) {
      ret += " {tok.mask_token} ";
      styledText +=
        "<span style='background-color: mediumblue; color: white;'>";
    } else ret += "{tok.mask_token} ";
  }
  styledText += text.substring(
    editor.prop("selectionStart"),
    editor.prop("selectionEnd")
  );
  styledText += "</span>";
  styledText += text.substring(editor.prop("selectionEnd"));
  // Get the rest of the text after the end of the selection
  ret += text.substring(editor.prop("selectionEnd"));
  return { text: ret, styledText: styledText };
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
  // When saving a prediction on the new project page,
  // must prompt user for a project name and save the project
  // first, then go through the steps of saving the prediction
  // and redirect user to saved project page
  let textID = window.location.pathname.split("/");
  textID = textID[3];
  const time = new Date().toLocaleString();
  if (textID === "newProject") {
    const textName = prompt("Enter a name for this text:");
    if (!textName) {
      let notyf = new Notyf();
      notyf.error("Must enter a text name to save");
      return;
    }
    const predictionName = prompt("Enter prediction name");
    if (!predictionName) {
      let predNotyf = new Notyf();
      predNotyf.error("Must enter prediction name");
      return; // Client must enter a name to save a prediction
    }
    // Get text content of the textarea
    text = $("#editor-div").prop("innerText");
    if (text == "") {
      let notyf = new Notyf();
      notyf.error("Can't save empty text");
      return;
    }
    userID = window.location.pathname.split("/");
    userID = userID[2];

    // Send data to server
    const saveTransfer = {
      user_id: userID,
      text: text,
      text_name: textName,
      time: time,
      new: "true",
    };
    request = $.post("/saveProject", saveTransfer, (response) => {
      if (response.startsWith("Error")) {
        let notyf = new Notyf();
        notyf.error(response);
        return;
      }
      textID = Number(response);
      // Save prediction
      const transfer = {
        prediction_name: predictionName,
        prediction: prediction,
        text_id: textID,
        save_time: time,
        prediction_blob: JSON.stringify(getPageState()),
        redirect: "true",
        user_id: userID,
      };
      request = $.post("/savePrediction", transfer, (response) => {
        window.location.href = response;
        let lastNotyf = new Notyf();
        lastNotyf.success("Prediction saved!");
      });
    });
    return;
  }

  // Save prediction
  const predictionName = prompt("Enter prediction name");
  if (!predictionName) return; // Client must enter a name to save a prediction
  const transfer = {
    prediction: prediction,
    prediction_name: predictionName,
    text_id: textID,
    save_time: time,
    prediction_blob: JSON.stringify(getPageState()),
  };
  console.log("TRANSFER", transfer);
  request = $.post("/savePrediction", transfer, handleSavePredictionResponse);
}

// Handles the response from saving a project
function handleSaveProjectResponse(response) {
  notyf = new Notyf();
  if (response.startsWith("Error")) {
    notyf.success(response);
  }
  else notyf.success("Project Saved");
}

// Handles a click of the save project button
function handleSaveProjectClick() {
  // console.log($("#text-name").prop("innerText"));
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
  console.log(window.location.pathname.split("/")[3])

  // Check if there is already a text name (true for projects that have
  // already been saved) or prompt user to enter one if not
  if ($("#text-name").prop("innerText")) {
    textName = $("#text-name").prop("innerText");
  } else {
    textName = prompt("Enter text name");
    if (!textName) return; // User must enter a text name to save a project
    textName = textName.trim(); // Remove trailing whitespace from names to avoid duplicate names
    // Send data to server
    transfer = {
      user_id: userID,
      text: text,
      text_name: textName,
      time: new Date().toLocaleString(),
      text_id: window.location.pathname.split("/")[3]
    };
    request = $.post("/saveProject", transfer, (response) => {
      if (response.startsWith("Error")) {
        let notyf = new Notyf();
        notyf.error(response);
        return;
      }
      window.location.href = response;
    });
    return;
  }

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
  if (response.startsWith("Error")) {
    let notyf = new Notyf();
    notyf.error(response);
    $("#prediction-output").html("");
    handleLockTextClick(); // simulate the unlocking
    return;
  }
  $("#prediction-output").html(response);
  document.getElementById("lock-button").style.display = "inline-block";
}

// Handles a click of the prediction button
function handlePredictClick() {
  const parent = document.getElementById("textarea-container");
  const child = parent.firstElementChild;
  let texts = null;
  console.log("ID:", child.id);
  if (child.id == "editor-div") {
    parent.innerHTML = "";
    console.log("AREA", textArea);
    parent.appendChild(textArea);
    texts = getHighlight();
    parent.innerHTML = "";
    parent.appendChild(child);
  } else {
    texts = getHighlight();
  }
  const text = texts["text"];
  if (!text) return;
  const numTokens = $("#token-number").val();
  $("#prediction-output").html(
    "<div style='display: flex; align-items: center; justify-content: center;'><span class='loader'></span></div>"
  );
  if (!textDiv) {
    textDiv = document.createElement("div");
    textDiv.id = "editor-div";
    textDiv.style.overflowY = "auto";
    textDiv.style.maxHeight = "100%";
    textDiv.style.fontFamily = "monospace";
  }
  textDiv.innerHTML = texts["styledText"].replaceAll("\n", "<br>"); // update textDiv
  if (child.id != "editor-div") textArea = document.getElementById("editor"); // save current textarea state
  parent.innerHTML = "";
  parent.appendChild(textDiv);
  transfer = {
    text: text,
    numTokens: numTokens,
    prefix: $("#prefix").val(),
    suffix: $("#suffix").val(),
  };
  request = $.post("/predict", transfer, handlePredictResponse);
}

// Handles a click of the lock button
function handleLockTextClick() {
  document.getElementById("lock-button").style.display = "none";
  document.getElementById("textarea-container").innerHTML = "";
  document.getElementById("textarea-container").appendChild(textArea);
  document.getElementById("prediction-output").innerHTML = "";
}

// Handles a click of a delete button for a prediction
// Removes the elements representing the prediction from the DOM
function handleDeleteClick(event) {
  const button = event.target;
  const ancestor = button.closest(".single-prediction-container");
  if (ancestor) ancestor.remove();
}

// Called when a save prediction button is clicked
// Gets the page state and information about the prediction
function getPageState() {
  let obj = {
    text: document.getElementById("textarea-container").innerHTML,
    prediction_output: document.getElementById("prediction-container")
      .innerHTML,
    numTokens: $("#token-number").val(),
    prefix: $("#prefix").val(),
    suffix: $("#suffix").val(),
  };
  return obj;
}
function refocus() {
  if (textArea) textArea.focus();
}
function handleLogOutClick() {
  console.log("logout clicked");
  $.get("/logout", (response) => {
    window.location.href = response;
  });
}

function handlePredictionDblClick(event) {
  let textID = window.location.pathname.split("/");
  textID = textID[3];
  const child = event.target;
  const ancestor = child.closest(".saved-prediction-text-container");
  const predictionName = ancestor.querySelector(
    ".saved-prediction-name"
  ).innerText;
  const transfer = {
    text_id: textID,
    prediction_name: predictionName.replace(":", ":"),
  };
  document.getElementById("lock-button").style.display = "inline-block";
  $.post("/populatePrediction", transfer, (response) => {
    const obj = JSON.parse(response);
    const blob = JSON.parse(obj["prediction_blob"]);
    document.getElementById("textarea-container").innerHTML = blob["text"];
    document.getElementById("prediction-container").innerHTML =
      blob["prediction_output"];
    document.getElementById("suffix").value = blob["suffix"];
    document.getElementById("prefix").value = blob["prefix"];
    document.getElementById("token-number").value = blob["numTokens"];
  });
}
function handleDeleteSavedPredictionClick(event) {
  const button = event.target;
  const ancestor = button.closest(".saved-prediction-container");
  const predictionName = ancestor.querySelector(
    ".saved-prediction-name"
  ).innerText;
  let textID = window.location.pathname.split("/");
  textID = textID[3];
  const transfer = {
    text_id: textID,
    prediction_name: predictionName.replaceAll(":", ":"),
  };
  $.post("/deletePrediction", transfer, (response) => {
    ancestor.remove();
  });
}
