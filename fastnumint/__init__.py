from .iter import *
from .newton_cotes import *
from .gauss_quadrature import *
from functools import lru_cache


def int_num(f, a, b, tol=1e-4, maxiter=1000):
    _integrate = composite_iter(gauss_quadrature)
    if b < a:
        return -_integrate(f, b, a, tol, maxiter)
    else:
        return _integrate(f, a, b, tol, maxiter)


def int_num_cachedf(f, a, b, tol=1e-4, maxiter=1000):
    return int_num(lru_cache(maxsize=None)(f), a, b, tol, maxiter)
