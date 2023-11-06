from functools import lru_cache
from bisect import insort

from .wynn_epsilon import WynnEpsilon


def orderab(func):
    """Ensures that a<=b."""

    def wrapper(f, a, b, *args, **kwargs):
        if b < a:
            return -func(f, b, a, *args, **kwargs)
        return func(f, a, b, *args, **kwargs)

    return wrapper


def cachedf(func):
    """Makes f cached."""

    def wrapper(f, *args, **kwargs):
        return func(lru_cache(maxsize=None)(f), *args, **kwargs)

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
    Takes a function `integrate: (f, a, b)->(integral_estimate, error_estimate)`
    that integrates `f` from `a` to `b` and returns estimates for the integral and error.
    Constructs a function `(f, a, b, tol, maxdepth)->float` that integrates `f` from `a` to `b`
    by bisecting each segment until its tolerance is low enough
    or a maximum recursion depth is reached.
    The resulting integral should have an error `<=tol`
    """

    def wrapper(f, a, b, tol, maxdepth):
        whole, err = integrate(f, a, b)
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
    by_integral = lambda e: e[2]
    by_error = lambda e: e[3]

    def wrapper(f, a, b, tol, maxiter):
        segments = [(a, b, *integrate(f, a, b))]
        for i in range(maxiter):
            if sum(map(by_error, segments)) <= tol:
                return sum(map(by_integral, segments))

            # bisect the segment with the largest error (the last segment)
            # and insert the new segments at the appropriate places
            a, b, _, _ = segments.pop()
            m = (a + b) / 2
            insort(segments, (a, m, *integrate(f, a, m)), key=by_error)
            insort(segments, (m, b, *integrate(f, m, b)), key=by_error)

        if sum(map(by_error, segments)) > tol:
            print_nonconvergence_warning()
        return sum(map(by_integral, segments))

    return wrapper


def global_adaptive_extrapolation(integrate):
    """
    A decorator for applying the adaptive extrapolation algorithm from
    de Doncker 1978 (https://doi.org/10.1145/1053402.1053403).
    Takes a function `integrate: (f, a, b)->(integral_estimate, error_estimate)`
    that integrates `f` from `a` to `b` and returns estimates for the integral and error.
    Constructs a function `(f, a, b, tol, maxdepth)->float` that integrates `f` from `a` to `b`
    using the algorithm outlined in the reference above.
    """
    by_integral = lambda e: e[2]
    by_error = lambda e: e[3]

    def _insort_bisected(segments, f, a, b, level):
        m = (a + b) / 2
        insort(segments, (a, m, *integrate(f, a, m), level), key=by_error)
        insort(segments, (m, b, *integrate(f, m, b), level), key=by_error)

    def wrapper(f, a, b, tol, maxiter):
        iteration = level = 0
        wynn = WynnEpsilon()
        segments = [(a, b, *integrate(f, a, b), level)]
        while sum(map(by_error, segments)) > tol:
            if iteration >= maxiter:
                print_nonconvergence_warning()
                break

            a, b, _, _, lvl = segments[-1]
            if lvl < level:
                # bisect the segment with the largest error
                del segments[-1]
                _insort_bisected(segments, f, a, b, lvl + 1)
                iteration += 1
            else:
                # the smallest segment has the largest error
                # decrease the error of the larger segments first
                long_segment = lambda seg: seg[4] < level
                while iteration < maxiter and sum(
                        map(by_error, filter(long_segment, segments))) > tol:
                    # bisect the segment with the largest error among the 'long' segments
                    a, b, _, _, lvl = _pop_last_where(long_segment, segments)
                    _insort_bisected(segments, f, a, b, lvl + 1)
                    iteration += 1

                # perform extrapolation
                wynn.add(sum(map(by_integral, segments)))
                if wynn.error <= tol:
                    return wynn.extrapolation

                level += 1

        return sum(map(by_integral, segments))

    return wrapper


def _pop_last_where(predicate, collection):
    """
    Pops the last element which fulfills a predicate from a collection.

    :param predicate: A predicate function for filtering elements.
    :param collection: The collection to pop the element from.
    :return: The popped element.
    """
    return collection.pop(
        next(filter(lambda e: predicate(e[1]), reversed(list(enumerate(collection)))))[0])
