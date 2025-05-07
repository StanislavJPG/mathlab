import functools


def tasks_decorator(func):
    """
    Wrapper that conveniently transform tuple of paths with crontabs and args to beat schedule API
    according to https://docs.celeryq.dev/en/latest/userguide/periodic-tasks.html#solar-schedules
    """

    @functools.wraps(func)
    def wrapper():
        args = func()

        def with_args(*t, args):
            return (
                t[0],
                (t[1], args),
            )

        args = [with_args(*arg, args=arg[-1]) if len(arg) == 3 else arg for arg in args]

        return {
            a.split('.')[-1]: {
                k: v
                for k, v in {'task': a, 'schedule': b, 'args': b[1] if isinstance(b, tuple) else None}.items()
                if v is not None
            }
            for a, b in args
        }

    return wrapper
