function explainMe(topic) {
  var url = `/mathlab/explainme/?topic=${encodeURIComponent(topic)}`;
  window.location.href = url;
}