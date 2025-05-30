
document.addEventListener('htmx:afterSettle', function () {
  var toastTriggers = document.querySelectorAll('[data-toast-trigger]');
  var toastLive = document.getElementById('liveToast');

  if (toastLive && toastTriggers.length > 0) {
    const toastBootstrap = bootstrap.Toast.getOrCreateInstance(
      toastLive,
      {autohide: false}
    );

    toastTriggers.forEach(trigger => {
      trigger.addEventListener('htmx:beforeRequest', () => {
        toastBootstrap.show();
      });

      trigger.addEventListener('htmx:afterRequest', () => {
        toastBootstrap.hide();
      });
    });
  }
});
