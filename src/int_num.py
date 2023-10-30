import math
from functools import lru_cache


def _print_nonconvergence_warning():
    print('----------------------------------')
    print('   WARNING: maxiter was reached   ')
    print('Your calculation did not converge!')
    print('----------------------------------')
    print()


def int_num(f, a, b, tol=1e-4, maxiter=1000):
    _integrate = _basic_iter(_booles_rule)
    if b < a:
        return -_integrate(f, b, a, tol, maxiter)
    else:
        return _integrate(f, a, b, tol, maxiter)


def int_num_cachedf(f, a, b, tol=1e-4, maxiter=1000):
    return int_num(lru_cache(maxsize=None)(f), a, b, tol, maxiter)


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
    segcount *= 2
    h = (b - a) / segcount
    xs = [a + i * h for i in range(segcount + 1)]
    area = sum((f(xs[i + 0]) + 4 * f(xs[i + 1]) + f(xs[i + 2])) for i in
               range(0, segcount, 2)) * h / 3
    return area


def _booles_rule(f, a, b, segcount):
    segcount *= 4
    h = (b - a) / segcount
    xs = [a + i * h for i in range(segcount + 1)]
    area = sum((7 * f(xs[i]) + 32 * f(xs[i + 1]) + 12 * f(xs[i + 2]) + 32 * f(xs[i + 3]) +
                7 * f(xs[i + 4])) for i in range(0, segcount, 4)) * h * 2 / 45
    return area
