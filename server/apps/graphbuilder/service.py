from numpy import ndarray


def my_func(x: ndarray, function: str) -> ndarray:
    """
    the main goal of the "my func" is to evaluate function using numpy objects

    :param x: this is X argument from function (ndarray object)
    :param function: this is whole function needs to solve and build
    :return: ndarray object (this is built graph)
    """
    try:
        return eval(function)
    except NameError:
        raise Exception('Invalid syntax.')
