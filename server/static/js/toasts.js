const toastTemplate = document.querySelector("[data-toast-template]");
const toastContainer = document.querySelector("[data-toast-container]");

function createToast(message) {
    const elem = toastTemplate.cloneNode(true);
    delete elem.dataset.toastTemplate;
    toastContainer.appendChild(elem);
    elem.className += " bg-" + message.tags;
    elem.querySelector("[data-toast-body]").innerHTML = `
      <i class="ti ${message.tags === 'success' ? 'ti-progress-check' : 'ti-exclamation-circle'}"></i> 
      ${message.message}
    `;

    elem.querySelector("[data-toast-body]").className += " text-light";

    const toast = new bootstrap.Toast(elem, {delay: 2000});
    toast.show();
}

document.addEventListener("htmx:afterRequest", function (event) {
    const redirectUrl = event.detail.xhr.getResponseHeader("HX-Redirect");
    if (redirectUrl) {
        const redirectUrl = event.detail.xhr.getResponseHeader("HX-Redirect");
        const toastElements = document.querySelectorAll("[data-toast-body]");
        const messages = [];

        if (toastElements.length > 0) {
            const lastMsg = toastElements[toastElements.length - 1]; // Get the last element

            messages.push({
                message: lastMsg.innerText,
                tags: lastMsg.dataset.toastTags || "success",
            });
        }

        if (messages.length > 0) {
            localStorage.setItem("flashMessages", JSON.stringify(messages));
        }

        window.location.href = redirectUrl;
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const storedMessages = localStorage.getItem("flashMessages");
    if (storedMessages) {
        JSON.parse(storedMessages).forEach(createToast);
        localStorage.removeItem("flashMessages");
    }
});

htmx.on("messages", (e) => {
    e.detail.value.forEach(createToast);
});
