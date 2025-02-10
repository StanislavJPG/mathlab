document.addEventListener("DOMContentLoaded", function() {
    var closeButton = document.getElementById("closeButton");
    if (closeButton) {
        closeButton.addEventListener("click", function() {
            closeButton.parentElement.style.display = "none";
        });
    }
});