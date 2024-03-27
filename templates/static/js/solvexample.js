function getRightCalculation(example, tofind, type) {
  var encodedExample = encodeURIComponent(example);
  window.location.href = `/solvexample/equations/?example=${encodedExample}&to-find=${tofind}&type=${type}`;
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
  window.location.href = `/solvexample/matrix/?matrixA=${encodedMatrixA}&matrixB=${encodedMatrixB}&operator=${encodedOperator}`;
}


function checkIsItMathSymbol(matrixA, matrixB, symbol) {
  if (typeof symbol === "string") {
    if (['+', '-', '**', '*', '>', '<', '>=', '<=', '=='].includes(symbol)) {
      getRightCalculationForMatrix(matrixA, matrixB, symbol);
    } else {
      alert('Тільки математичні символи дій над матрицями!')
      throw new Error('Only symbols');
    }
  } else {
    alert('Тільки математичні символи дій над матрицями!')
    throw new Error('Only symbols');
  }
}


