var notify_menu_class;
var notify_menu_el_class;

function bs_fill_notification_list(data) {
    var menus = document.getElementsByClassName(notify_menu_class);
    if (menus) {
        if (data.unread_list.length !== 0) {
            var messages = data.unread_list.map(function (item) {
                var message = "";

                if (typeof item.actor !== 'undefined') {
                    message = `<strong>${item.actor_display_name}</strong>`;
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
                return `<li><hr class="dropdown-divider"></li><li><a class="${notify_menu_el_class}" href="${item.action_url}" style="font-size: 14px;">${message}</a></li>`;
            }).join('')
            var clear_all_btn = `
                <a href="javascript:(0);"
                   hx-post="theorist/notifications/mark-all-read/"
                   hx-target="#noti-badge"
                   hx-trigger="click delay:0.5s"
                   class="small text-end d-block text-decoration-none me-2">
                <i class="ti ti-square-rounded-x"></i> ${gettext('Clear all messages')}</a>
            `;
        } else {
            messages = `<li><span class="dropdown-item-text small text-muted text-nowrap">${gettext('No unread notifications yet')}</span></li>`
        }

        for (var i = 0; i < menus.length; i++) {
            menus[i].innerHTML = clear_all_btn ? clear_all_btn : '';
            menus[i].innerHTML += messages;
            menus[i].innerHTML += '<hr class="mt-2 mb-2"/><div class="d-grid gap-2">' +
            `<a type="button" target="_blank" href="theorist/notifications/all/" class="btn btn-outline-primary btn-sm text-center d-block"><i class="ti ti-notification"></i> ${gettext('Read all notifications')}</a>` +
            '</div>';
            htmx.process(menus[i]);
        }
    }
}