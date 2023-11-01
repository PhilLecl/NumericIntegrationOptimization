from .gauss_legendre import abscissae as glabscissae, weights as glweights


def gauss_legendre(f, a, b, n=5):
    scaling = (b - a) / 2
    midpoint = (a + b) / 2
    return sum(
        f(scaling * xi + midpoint) * wi for xi, wi in zip(glabscissae[n], glweights[n])) * scaling


def _agl(f, a, b, n, whole, tol, maxdepth):
    if maxdepth <= 0:
        return whole
    left = gauss_legendre(f, a, (a + b) / 2, n)
    right = gauss_legendre(f, (a + b) / 2, b, n)
    delta = left + right - whole
    if abs(delta) <= tol:
        return left + right
    else:
        return _agl(f, a, (a + b) / 2, n, left, tol / 2, maxdepth - 1) + \
            _agl(f, (a + b) / 2, b, n, right, tol / 2, maxdepth - 1)


def local_adaptive_gauss_legendre(f, a, b, tol, maxdepth, n=5):
    return _agl(f, a, b, n, gauss_legendre(f, a, b, n), tol, maxdepth - 1)
