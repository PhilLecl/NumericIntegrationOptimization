from .gauss_quadrature.gauss_kronrod import global_adaptive as gagk, local_adaptive as lagk
from .gauss_quadrature.gauss_legendre import iterative as igl, local_adaptive as lagl
from .newton_cotes import *
from functools import lru_cache


def int_num(f, a, b, tol=1e-4, maxiter=1000):
    return gagk()(f, a, b, tol, maxiter)


def int_num_cachedf(f, a, b, tol=1e-4, maxiter=1000):
    return int_num(lru_cache(maxsize=None)(f), a, b, tol, maxiter)
