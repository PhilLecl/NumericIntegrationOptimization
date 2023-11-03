from .iter import *
from .newton_cotes import *
from fastnumint.gauss_quadrature import *
from functools import lru_cache


def int_num(f, a, b, tol=1e-4, maxiter=1000):
    if b < a:
        return -int_num(f, b, a, tol, maxiter)
    return basic_iter(booles_rule)(f, a, b, tol, maxiter)


def int_num_cachedf(f, a, b, tol=1e-4, maxiter=1000):
    return int_num(lru_cache(maxsize=None)(f), a, b, tol, maxiter)
