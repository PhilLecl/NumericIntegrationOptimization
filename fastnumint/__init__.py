from .gauss_quadrature.gauss_kronrod import global_adaptive as gagk, local_adaptive as lagk, \
    global_adaptive_wynn as gaegk
from .gauss_quadrature.gauss_legendre import iterative as igl, local_adaptive as lagl
from .newton_cotes import *


def int_num(f, a, b, tol=1e-4, maxiter=1000):
    return gaegk(21)(f, a, b, tol, maxiter)
