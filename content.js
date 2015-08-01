chrome.runtime.sendMessage({
  'url': window.location.href,
  'text': window.getSelection().toString(),
  'title': document.title
});
