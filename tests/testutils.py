def is_too_long_input(response, field: str) -> bool:
    if not isinstance(field, str):
        raise ValueError('field must be a string')

    # in UA local. Maybe add i18n in the future
    return 'Переконайтеся, що це значення' in response.get_form().errors[field][0]
