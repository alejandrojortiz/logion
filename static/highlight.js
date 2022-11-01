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
getHighlight = () => {
  // Get text
  const editor = $("#editor");
  let text = editor.val();
  if (!text) return;

  // Replace selection with the appropriate number of tokens
  const numTokens = $("#token-number").val();
  let ret = text.substring(0, editor.selectionStart);
  for (let i = 0; i < numTokens; i++) {
    ret += "{tok.mask_token}";
  }
  if (editor.selectionEnd + 1 < text.length()) {
    ret += text.substring(editor.selectionEnd + 1);
  }

  return ret;
};
