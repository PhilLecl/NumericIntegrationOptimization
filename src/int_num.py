import math
from functools import lru_cache


def _print_nonconvergence_warning():
    print('----------------------------------')
    print('   WARNING: maxiter was reached   ')
    print('Your calculation did not converge!')
    print('----------------------------------')
    print()


def int_num(f, a, b, tol=1e-4, maxiter=1000):
    _integrate = _cachef(_basic_iter(_simpsons_rule))
    if b < a:
        return -_integrate(f, b, a, tol, maxiter)
    else:
        return _integrate(f, a, b, tol, maxiter)


def _basic_iter(calc_area, init_segcount=4):
    def wrapper(f, a, b, tol, maxiter):
        segcount = init_segcount
        area = calc_area(f, a, b, segcount)
        for iteration in range(maxiter):
            old_area = area
            segcount *= 2
            area = calc_area(f, a, b, segcount)
            if abs(area - old_area) <= tol:
                break
        if iteration == maxiter - 1:
            _print_nonconvergence_warning()
        return area

    return wrapper


def _cachef(func):
    def wrapper(f, *args):
        f = lru_cache(maxsize=None)(f)
        return func(f, *args)

    return wrapper


def _rectangle_rule(f, a, b, segcount):
    segwidth = (b - a) / segcount
    xs = [a + (i + 0.5) * segwidth for i in range(segcount)]
    area = sum(f(xs[i]) for i in range(segcount)) * segwidth
    return area


def _trapezoidal_rule(f, a, b, segcount):
    segwidth = (b - a) / segcount
    xs = [a + i * segwidth for i in range(segcount + 1)]
    area = sum((f(xs[i]) + f(xs[i + 1])) for i in range(segcount)) * segwidth / 2
    return area


def _simpsons_rule(f, a, b, segcount):
    segwidth = (b - a) / segcount
    xs = [a + i * segwidth for i in range(segcount + 1)]
    area = sum(_simpson_segment(f, xs[i], xs[i + 1]) for i in range(segcount))
    return area


def _simpson_segment(f, a, b):
    h = (b - a) / 2
    xs = [a + i * h for i in range(3)]
    area = (f(xs[0]) + 4 * f(xs[1]) + f(xs[2])) * h / 3
    return area
