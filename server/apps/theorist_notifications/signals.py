from server.common.utils.helpers import is_iterable


class ExtendedNotificationSignal:
    def send(self, sender, **kwargs):
        recipients = kwargs.get('recipient')
        if is_iterable(recipients):
            for recipient in set(recipients):
                kwargs['recipient'] = recipient
                self._process_sending(sender, **kwargs)
        else:  # keep logic for single recipient notification
            self._process_sending(sender, **kwargs)

    def _process_sending(self, sender, **kwargs):
        from notifications.signals import notify

        self.sender = sender

        is_notification_passed = self._pass_notification(**kwargs)

        if is_notification_passed:
            extended_kwargs = self._extend_kwargs_by_defaults(**kwargs)
            send = notify.send(sender, **extended_kwargs)

            self._get_obj_notification(send).extend_notification(
                action_url=extended_kwargs['action_url'], target_display_name=extended_kwargs['target_display_name']
            )
            return send

    def _exclude_sender(self, **kwargs):
        recipient = kwargs.get('recipient')
        if hasattr(recipient, 'theorist'):
            return self.sender == recipient.theorist

    def _pass_notification(self, **kwargs):
        recipient = kwargs.get('recipient')
        if self._exclude_sender(**kwargs):
            return False
        if hasattr(recipient, 'theorist'):
            return recipient.theorist.settings.is_able_to_receive_notifications

        return False

    @staticmethod
    def _extend_kwargs_by_defaults(**kwargs):
        kwargs.update(
            {
                'verb': kwargs.get('verb', ''),
                'action_url': kwargs.get('action_url', None),
                'target_display_name': kwargs.get('target_display_name', None),
            }
        )
        return kwargs

    @staticmethod
    def _get_obj_notification(notify_send_obj):
        # take default just created obj from notify.send()
        return notify_send_obj[0][1][0]


notify = ExtendedNotificationSignal()
