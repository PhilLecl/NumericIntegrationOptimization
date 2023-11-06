from fastnumint import newton_cotes
from fastnumint.gauss_quadrature import gauss_kronrod, gauss_legendre


def int_num(f, a, b, tol=1e-4, maxiter=1000):
    return gauss_kronrod.global_adaptive(21)(f, a, b, tol, maxiter)
