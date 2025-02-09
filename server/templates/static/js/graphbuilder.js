document.getElementById("showPopupButton").addEventListener("click", function() {
    document.getElementById("popupContainer").style.display = "block";
});
document.getElementById("closePopup").addEventListener("click", function() {
    document.getElementById("popupContainer").style.display = "none";
});

function graphBuilder(func) {
  var url = `/graphbuilder/?function=${encodeURIComponent(func)}`;

  fetch(url)
    .then(response => {
      if (response.status === 200) {
        window.location.href = url;
      } else {
        throw new Error('Response status is not 200');
      }
    })
    .catch(error => {
      alert('Помилка. Перевірте правильність введеної функції. \nПрочитайте вказівники.');
    });
}