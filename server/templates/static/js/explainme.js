function explainMe(topic) {
  var url = `/explainme/?topic=${encodeURIComponent(topic)}`;
  window.location.href = url;
}