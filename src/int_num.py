import math
from functools import lru_cache


def _print_nonconvergence_warning():
    print('----------------------------------')
    print('   WARNING: maxiter was reached   ')
    print('Your calculation did not converge!')
    print('----------------------------------')
    print()


def int_num(f, a, b, tol=1e-4, maxiter=1000):
    _integrate = _rechteck
    if b < a:
        return -_integrate(f, b, a, tol, maxiter)
    else:
        return _integrate(f, a, b, tol, maxiter)


def _rechteck(f, a, b, tol, maxiter):
    segcount = 4
    area = _rechtecksformel(f, a, b, segcount)
    for iteration in range(maxiter):
        old_area = area
        segcount *= 2
        area = _rechtecksformel(f, a, b, segcount)
        if abs(area - old_area) <= tol:
            break
    if iteration == maxiter - 1:
        _print_nonconvergence_warning()
    return area


def _rechtecksformel(f, a, b, segcount):
    segwidth = (b - a) / segcount
    xs = [a + (i + 0.5) * segwidth for i in range(segcount)]
    area = sum(f(xs[i]) for i in range(segcount)) * segwidth
    return area
