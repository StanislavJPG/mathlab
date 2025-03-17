import functools


def periodic_tasks_args(func):
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
