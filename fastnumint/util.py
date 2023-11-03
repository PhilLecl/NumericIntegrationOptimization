def orderab(func):
    """Ensures that a<=b."""

    def wrapper(f, a, b, tol, maxiter):
        if b < a:
            return -wrapper(f, b, a, tol, maxiter)
        return func(f, a, b, tol, maxiter)

    return wrapper


def print_nonconvergence_warning():
    print('----------------------------------')
    print('   WARNING: maxiter was reached   ')
    print('Your calculation did not converge!')
    print('----------------------------------')
    print()


def basic_iter(init_segcount=4):
    """
    A decorator for iteratively doubling the number of segments until convergence is reached.
    Takes a function `(f, a, b, segcount)->float`
    for integrating `f` from `a` to `b` using `segcount` segments.
    Constructs a function `(f, a, b, tol, maxiter)->float` that integrates `f` from `a` to `b`
    by iteratively doubling the number of segments until `segcount` iterations have been reached
    or the error is estimated to be below `tol`.

    :param init_segcount: The initial number of segments.
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
    Takes a function `(f, a, b)->float` for integrating `f` from `a` to `b`.
    Constructs a function `(f, a, b, tol, maxiter)->float` that integrates `f` from `a` to `b`
    by iteratively doubling the number of segments until `segcount` iterations have been reached
    or the error is estimated to be below `tol`.

    :param init_segcount: The initial number of segments.
    """

    def decorator(func):
        def wrapper(f, a, b, tol, maxiter):
            segcount = init_segcount
            area = _segment(segcount)(func)(f, a, b)
            for _ in range(maxiter):
                old_area = area
                segcount *= 2
                area = _segment(segcount)(func)(f, a, b)
                if abs(area - old_area) <= tol:
                    return area
            print_nonconvergence_warning()
            return area

        return wrapper

    return decorator


def _segment(segcount=2):
    """
    A decorator for calculating an integral in `segcount` segments.
    Takes a function `integrate: (f, a, b)->float` for integrating f from `a` to `b`.
    Constructs a function `(f, a, b)->float` that integrates `f` from `a` to `b`
    by splitting that interval into `segcount` segments and applying `integrate` to each one.

    :param segcount: The number of segments.
    """

    def decorator(integrate):
        def wrapper(f, a, b):
            h = (b - a) / segcount
            xs = [a + i * h for i in range(segcount + 1)]
            return sum(integrate(f, xs[i], xs[i + 1]) for i in range(segcount))

        return wrapper

    return decorator


def local_adaptive(integrate):
    """
    A decorator for making a function locally adaptive.
    Takes a function `integrate: (f, a, b)->(a, b, integral_estimate, error_estimate)`
    that integrates `f` from `a` to `b`
    and returns `a`, `b` and estimates for the integral and error.
    Constructs a function `(f, a, b, tol, maxdepth)->float` that integrates `f` from `a` to `b`
    by bisecting each segment until its tolerance is low enough
    or a maximum recursion depth is reached.
    The resulting integral should have an error `<=tol`
    """

    def wrapper(f, a, b, tol, maxdepth):
        _, _, whole, err = integrate(f, a, b)
        if not maxdepth or err <= tol:
            return whole
        m = (a + b) / 2
        return wrapper(f, a, m, tol / 2, maxdepth - 1) + \
            wrapper(f, m, b, tol / 2, maxdepth - 1)

    return wrapper


def global_adaptive(integrate):
    """
    A decorator for making a function globally adaptive.
    Takes a function `integrate: (f, a, b)->(a, b, integral_estimate, error_estimate)`
    that integrates `f` from `a` to `b`
    and returns `a`, `b` and estimates for the integral and error.
    Constructs a function `(f, a, b, tol, maxiter)->float` that integrates `f` from `a` to `b`
    by iteratively bisecting the segment with the largest error-estimate
    until the sum of error-estimates is `<=tol` or `maxiter` iterations have been reached.
    """

    def wrapper(f, a, b, tol, maxiter):
        segments = [integrate(f, a, b)]
        for i in range(maxiter):
            if sum(e for (a, b, segint, e) in segments) <= tol:
                return sum(segint for (a, b, segint, e) in segments)

            # bisect the segment with the largest error
            i, (a, b, segint, e) = max(enumerate(segments), key=lambda el: el[1][3])
            m = (a + b) / 2
            segments = segments[:i] + [integrate(f, a, m)] + [integrate(f, m, b)] + segments[
                                                                                    i + 1:]

        if sum(e for (a, b, segint, e) in segments) > tol:
            print_nonconvergence_warning()
        return sum(segint for (a, b, segint, e) in segments)

    return wrapper
