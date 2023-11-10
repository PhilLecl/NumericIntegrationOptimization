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
        err, whole = integrate(f, a, b)
        if not maxdepth or err <= tol:
            return whole
        m = (a + b) / 2
        return wrapper(f, a, m, tol / 2, maxdepth - 1) + \
            wrapper(f, m, b, tol / 2, maxdepth - 1)

    return wrapper


def global_adaptive(integrate):
    """
    A decorator for making a function globally adaptive.
    Takes a function `integrate: (f, a, b)->(error_estimate, integral_estimate)`
    that integrates `f` from `a` to `b`.
    Constructs a function `(f, a, b, tol, maxiter)->float` that integrates `f` from `a` to `b`
    by iteratively bisecting the segment with the largest error-estimate
    until the sum of error-estimates is `<=tol` or `maxiter` iterations have been reached.

    If `integrate` would return the negative of the error-estimate,
    `bisect.insort` could be replaced by `heapq` (`heappop`&`heappush`).
    It's hard to tell which one is faster.
    As `insort` is better for compatibility with `global_adaptive_extrapolation`,
    I'm keeping it for now.
    """

    def wrapper(f, a, b, tol, maxiter):
        segments = [(*integrate(f, a, b), a, b)]  # each segment is a tuple (error, integral, a, b)
        errsum = segments[0][0]  # manual updates are slightly faster than recomputing on-the-fly
        if errsum > tol:
            for i in range(maxiter):
                # bisect the segment with the largest error (= the last element)
                err, _, a, b = segments.pop()
                m = (a + b) / 2  # midpoint of the segment
                left, right = (*integrate(f, a, m), a, m), (*integrate(f, m, b), m, b)
                # insert the new segments while keeping the list sorted by ascending error
                insort(segments, left)
                insort(segments, right)
                # update sum of errors and check for convergence
                errsum += left[0] + right[0] - err
                if errsum <= tol:
                    break
            else:  # slightly cursed Python syntax for "no break occurred" (= no convergence)
                print_nonconvergence_warning()
        return sum(I for _, I, _, _ in segments)

    return wrapper


def global_adaptive_extrapolation(integrate):
    """
    A decorator for applying the adaptive extrapolation algorithm from
    de Doncker 1978 (https://doi.org/10.1145/1053402.1053403).
    Takes a function `integrate: (f, a, b)->(error_estimate, integral_estimate)`
    that integrates `f` from `a` to `b`.
    Constructs a function `(f, a, b, tol, maxdepth)->float` that integrates `f` from `a` to `b`
    using the algorithm outlined in the reference above.
    """

    def _bisect_segment(segments, f, err, I, a, b, lvl):
        """
        Bisect a segment, insort the new segments and return the change of the error-estimate.
        The params after `f` are ordered so that one can pass an unpacked `*segment`.

        :param segments: The list of segments to insort the new segments in
        :param f: The function to be integrated
        :param err: The error-estimate of the segment to be bisected
        :param I: The integral-estimate of the segment to be bisected
        :param a: The lower bound of the segment to be bisected
        :param b: The upper bound of the segment to be bisected
        :param lvl: The bisection-level of the segment to be bisected
        :return: The change in error-estimate
        """
        m = (a + b) / 2
        left, right = (*integrate(f, a, m), a, m, lvl + 1), (*integrate(f, m, b), m, b, lvl + 1)
        insort(segments, left)
        insort(segments, right)
        return left[0] + right[0] - err

    def wrapper(f, a, b, tol, maxiter):
        iteration = level = 0
        wynn = WynnEpsilon()
        segments = [(*integrate(f, a, b), a, b, level)]
        errsum = segments[0][0]  # manual updates are slightly faster than recomputing on-the-fly
        while errsum > tol:
            if iteration >= maxiter:
                print_nonconvergence_warning()
                break

            lvl = segments[-1][4]
            if lvl < level:
                # bisect the segment with the largest error
                errsum += _bisect_segment(segments, f, *segments.pop())
                iteration += 1
            else:
                # the smallest segment has the largest error
                # decrease the error of the larger segments first
                long_segment = lambda seg: seg[4] < level
                # manually updating the sum-of-errors for the long segments might be faster,
                # but it's a pain-in-the-***, so I'm not doing it
                while iteration < maxiter and sum(
                        err for err, _, _, _, _ in filter(long_segment, segments)) > tol:
                    # bisect the segment with the largest error among the 'long' segments
                    errsum += _bisect_segment(segments, f,
                                              *_pop_last_where(long_segment, segments))
                    iteration += 1

                # perform extrapolation
                wynn.add(sum(I for _, I, _, _, _ in segments))  # TODO on-the-fly summation?
                if wynn.error <= tol:
                    return wynn.extrapolation

                level += 1

        return sum(I for _, I, _, _, _ in segments)

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
