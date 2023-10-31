from .iter import basic_iter
from .newton_cotes import _booles_rule, _simpsons_rule, _rectangle_rule
from functools import lru_cache


def int_num(f, a, b, tol=1e-4, maxiter=1000):
    _integrate = basic_iter(_booles_rule)
    if b < a:
        return -_integrate(f, b, a, tol, maxiter)
    else:
        return _integrate(f, a, b, tol, maxiter)


def int_num_cachedf(f, a, b, tol=1e-4, maxiter=1000):
    return int_num(lru_cache(maxsize=None)(f), a, b, tol, maxiter)
