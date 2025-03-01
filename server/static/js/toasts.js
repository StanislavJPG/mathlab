const toastTemplate = document.querySelector("[data-toast-template]")
const toastContainer = document.querySelector("[data-toast-container]")

function createToast(message) {
    const elem = toastTemplate.cloneNode(true)
    delete elem.dataset.toastTemplate
    toastContainer.appendChild(elem)
    elem.className += " bg-" + message.tags
    elem.querySelector("[data-toast-body]").innerHTML = `
      <i class="ti ${message.tags === 'success' ? 'ti-progress-check' : 'ti-exclamation-circle'}"></i> 
      ${message.message}
    `;

    elem.querySelector("[data-toast-body]").className += " text-light"

    const toast = new bootstrap.Toast(elem, {delay: 2000})
    toast.show()
}

htmx.on("messages", (e) => {
    e.detail.value.forEach(createToast)
})
