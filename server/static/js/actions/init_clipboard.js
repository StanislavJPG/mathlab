var clipboard = new ClipboardJS('.btn-to-copy');
clipboard.on('success', function (e) {
    const msg = {
        message: gettext('Copied to clipboard'),
        tags: 'success'
    }
    createToast(msg);
    e.clearSelection();
});