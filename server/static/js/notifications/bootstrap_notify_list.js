var notify_menu_class;
var notify_menu_el_class;

function bs_fill_notification_list(data) {
    var menus = document.getElementsByClassName(notify_menu_class);
    if (menus) {
        if (data.unread_list.length !== 0) {
            var messages = data.unread_list.map(function (item) {
                var message = "";

                if (typeof item.actor !== 'undefined') {
                    message = item.actor_display_name;
                }
                if (typeof item.verb !== 'undefined') {
                    message += " " + item.verb;
                }
                if (typeof item.target !== 'undefined') {
                    message += " " + item.target_display_name;
                }
                if (typeof item.timestamp !== 'undefined') {
                    var date = new Date(item.timestamp);
                    var intlDate = new Intl.DateTimeFormat("uk-UK", {
                        weekday: "long", year: "numeric", month: "long", day: "numeric"
                    }).format(date);
                    var formattedDate = gettext("Send at") + " " + intlDate;
                    message += "<br/>" + "<small class='text-muted'>- " + formattedDate + "</small>"
                }
                return `<li><a class="${notify_menu_el_class}" href="${item.action_url}" style="font-size: 14px;">${message}</a></li><li><hr class="dropdown-divider"></li>`;
            }).join('')
        }else{
            messages = `<li><span class="dropdown-item-text small text-muted text-nowrap">${gettext('Have no unread notifications yet')}</span></li>`
        }

        for (var i = 0; i < menus.length; i++) {
            menus[i].innerHTML = messages;
        }
    }
}