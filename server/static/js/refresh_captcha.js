$('#refresh-captcha').click(function () {
    $.getJSON("/captcha/refresh/", function (result) {
        $('.captcha').attr('src', result['image_url']);
        $('#id_captcha_0').val(result['key']);
    });
}); // see: https://django-simple-captcha.readthedocs.io/en/latest/usage.html