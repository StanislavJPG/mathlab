// issuer: https://github.com/bigskysoftware/htmx/issues/2029#issuecomment-1872067366
document.addEventListener("htmx:confirm", function (e) {
    e.preventDefault();
    if (!e.target.hasAttribute('hx-confirm')) {
        e.detail.issueRequest(true);
        return;
    }
    const theme = localStorage.getItem("theme");
    Swal.fire({
        title: gettext("Proceed?"),
        text: `${e.detail.question}`,
        icon: "warning",
        theme: (theme === "auto") ? "light" : theme,
        showCancelButton: true,
        confirmButtonText: gettext("Yes"),
        cancelButtonText: gettext("No"),
        reverseButtons: true
    }).then(function (result) {
        if (result.isConfirmed) e.detail.issueRequest(true); // use true to skip window.confirm
    });
});