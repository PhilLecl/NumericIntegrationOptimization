def print_nonconvergence_warning():
    print('----------------------------------')
    print('   WARNING: maxiter was reached   ')
    print('Your calculation did not converge!')
    print('----------------------------------')
    print()


def basic_iter(init_segcount=4):
    """
    A decorator for iteratively doubling the number of segments until convergence is reached.
    Takes a function (f, a, b, segcount)->float
    for integrating f from a to b using segcount segments.
    Constructs a function (f, a, b, tol, maxiter)->float that integrates f from a to b
    by iteratively doubling the number of segments until segcount iterations have been reached
    or the error is estimated to be below tol.

    :param init_segcount: The initial number of segments.
    :return:
    """

    def decorator(func):
        def wrapper(f, a, b, tol, maxiter):
            segcount = init_segcount
            area = func(f, a, b, segcount)
            for _ in range(maxiter):
                old_area = area
                segcount *= 2
                area = func(f, a, b, segcount)
                if abs(area - old_area) <= tol:
                    return area
            print_nonconvergence_warning()
            return area

        return wrapper

    return decorator


def composite_iter(init_segcount=1):
    """
    A decorator for iteratively doubling the number of segments until convergence is reached.
    Takes a function (f, a, b)->float for integrating f from a to b.
    Constructs a function (f, a, b, tol, maxiter)->float that integrates f from a to b
    by iteratively doubling the number of segments until segcount iterations have been reached
    or the error is estimated to be below tol.

    :param init_segcount: The initial number of segments.
    :return:
    """

    def decorator(func):
        def wrapper(f, a, b, tol, maxiter):
            segcount = init_segcount
            area = _composite(func, segcount)(f, a, b)
            for _ in range(maxiter):
                old_area = area
                segcount *= 2
                area = _composite(func, segcount)(f, a, b)
                if abs(area - old_area) <= tol:
                    return area
            print_nonconvergence_warning()
            return area

        return wrapper

    return decorator


def _composite(calc_area, segcount):
    def wrapper(f, a, b):
        h = (b - a) / segcount
        xs = [a + i * h for i in range(segcount + 1)]
        return sum(calc_area(f, xs[i], xs[i + 1]) for i in range(segcount))

    return wrapper
