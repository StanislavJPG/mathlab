// issuer: https://github.com/bigskysoftware/htmx/issues/2029#issuecomment-1872067366
document.addEventListener("htmx:confirm", function (e) {
    e.preventDefault();
    if (!e.target.hasAttribute('hx-confirm')) {
        e.detail.issueRequest(true);
        return;
    }
    Swal.fire({
        title: "Proceed?",
        text: `${e.detail.question}`,
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Yes",
        cancelButtonText: "No",
        reverseButtons: true
    }).then(function (result) {
        if (result.isConfirmed) e.detail.issueRequest(true); // use true to skip window.confirm
    });
});