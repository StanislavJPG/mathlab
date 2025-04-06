from django.utils.translation import gettext_lazy as _


def get_i18n_instance_name(instance_name):
    capitalized_instance_name = instance_name.capitalize()
    return _(capitalized_instance_name)
