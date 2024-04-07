function getRightCalculation(example, tofind, type) {
  var encodedExample = encodeURIComponent(example);
  var url = `/solvexample/equations/?example=${encodedExample}&to-find=${tofind}&type=${type}`;

  fetch(url)
    .then(response => {
      if (response.status === 200) {
        window.location.href = url;
      } else {
        throw new Error('Response status is not 200');
      }
    })
    .catch(error => {
      alert('Помилка. Перевірте правильність введених прикладів.\nПрочитайте вказівники.');
    });
}



document.getElementById("showPopupButton").addEventListener("click", function() {
    document.getElementById("popupContainer").style.display = "block";
});
document.getElementById("closePopup").addEventListener("click", function() {
    document.getElementById("popupContainer").style.display = "none";
});


function getRightCalculationForMatrix(matrixA, matrixB, operator) {
  var encodedMatrixA = encodeURIComponent(matrixA);
  var encodedMatrixB = encodeURIComponent(matrixB);
  var encodedOperator = encodeURIComponent(operator);
  var url = `/solvexample/matrix/?matrixA=${encodedMatrixA}&matrixB=${encodedMatrixB}&operator=${encodedOperator}`;

  fetch(url)
    .then(response => {
      if (response.status === 200) {
        window.location.href = url;
      } else {
        throw new Error('Response status is not 200');
      }
    })
    .catch(error => {
      alert('Помилка. Перевірте правильність введених матриць');
    });
}



function checkIsItMathSymbol() {
    var matrixA = document.getElementById('matrixA').value;
    var matrixB = document.getElementById('matrixB').value;
    var selectedOperation;

    var radioButtons = document.getElementsByName('option');
    for (var i = 0; i < radioButtons.length; i++) {
        if (radioButtons[i].checked) {
            selectedOperation = radioButtons[i].value;
            break;
        }
    }
    if (typeof selectedOperation === "string") {
        if (['+', '-', '*'].includes(selectedOperation)) {
            getRightCalculationForMatrix(matrixA, matrixB, selectedOperation);
        } else {
            alert('Тільки математичні символи дій над матрицями!')
            throw new Error('Only symbols');
        }
    } else {
        alert('Тільки математичні символи дій над матрицями!')
        throw new Error('Only symbols');
    }
}

function getRightPercentsCalculation(example, percent, num, type) {
  var encodedExample = encodeURIComponent(example);
  var url = `/solvexample/percents/?example=${example}&percent=${percent}&num=${num}&type=${type}`;

  fetch(url)
    .then(response => {
      if (response.status === 200) {
        window.location.href = url;
      } else {
        throw new Error('Response status is not 200');
      }
    })
    .catch(error => {
      alert('Помилка. Перевірте правильність введених прикладів');
    });
}



