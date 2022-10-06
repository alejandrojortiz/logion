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
let textarea = false;
const changeButton = document.getElementById("handler-button");
const statusBox = document.getElementById("status-box");
const DEBOUNCE_DURATION = 100;
changeButton.addEventListener("click", handleChangeButton);
document.addEventListener(
  "selectionchange",
  debounce(getNonTextAreaSelection, DEBOUNCE_DURATION)
);
function getNonTextAreaSelection() {
  // get the parent node of the selection, and then get its id
  const parent = document.getSelection().anchorNode.parentElement;
  const grandParent = parent.parentElement;
  const id = grandParent.getAttribute("id");
  const output = document.getElementById("output-paragraph");

  // only want to run the function if the parent element has the id we want
  // i.e. the selected text is in the container we use to limit which text can
  // be selected
  if (id != "selection-container") return;
  let selection = document.getSelection
    ? document.getSelection().toString()
    : document.selection.createRange().toString();
  if (selection) output.textContent = selection;
}
function getTextAreaSelection() {
  const editor = document.getElementById("editor");
  const text = editor.value;
  const output = document.getElementById("output-paragraph");

  if (!text) return;
  const result = text.substring(editor.selectionStart, editor.selectionEnd);
  if (result) output.textContent = result;
}
function handleChangeButton() {
  textarea = !textarea;
  if (textarea) {
    document.removeEventListener(
      "selectionchange",
      debounce(getNonTextAreaSelection, DEBOUNCE_DURATION)
    );
    document.addEventListener(
      "selectionchange",
      debounce(getTextAreaSelection, DEBOUNCE_DURATION)
    );
    statusBox.style =
      "margin: 0; display: inline-block; width: 1em; height: 1em; color: green;";
    statusBox.innerHTML = "&#10003"; // check
  } else {
    document.removeEventListener(
      "selectionchange",
      debounce(getTextAreaSelection, DEBOUNCE_DURATION)
    );
    document.addEventListener(
      "selectionchange",
      debounce(getNonTextAreaSelection, DEBOUNCE_DURATION)
    );
    statusBox.style =
      "margin: 0; display: inline-block; width: 1em; height: 1em; color: red;";
    statusBox.innerHTML = "&#10005"; // X
  }
}
