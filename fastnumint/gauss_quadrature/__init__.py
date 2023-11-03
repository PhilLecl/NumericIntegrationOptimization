from .gauss_legendre import abscissae as glabscissae, weights as glweights
from .gauss_kronrod import nodes as gknodes
from ..iter import print_nonconvergence_warning


def gauss_legendre(f, a, b, n=5):
    scaling = (b - a) / 2
    midpoint = (a + b) / 2
    return sum(
        f(scaling * xi + midpoint) * wi for xi, wi in zip(glabscissae[n], glweights[n])) * scaling


def _agl(f, a, b, n, whole, tol, maxdepth):
    if not maxdepth:
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


def gauss_kronrod(f, a, b, kronrod_degree):
    scaling = (b - a) / 2
    midpoint = (a + b) / 2
    nodes = [f(scaling * x + midpoint) for x, _, _ in gknodes[kronrod_degree]]
    gauss = sum(n * wg for n, (_, _, wg) in zip(nodes, gknodes[kronrod_degree]) if wg) * scaling
    kronrod = sum(n * wk for n, (_, wk, _) in zip(nodes, gknodes[kronrod_degree])) * scaling
    return a, b, kronrod, abs(kronrod - gauss)


def global_adaptive_gauss_kronrod(f, a, b, tol, maxiter, n=15):
    segments = [gauss_kronrod(f, a, b, n)]
    for i in range(maxiter):
        if sum(e for (a, b, segint, e) in segments) <= tol:
            return sum(segint for (a, b, segint, e) in segments)

        # bisect the segment with the largest error
        i, (a, b, segint, e) = max(enumerate(segments), key=lambda el: el[1][3])
        m = (a + b) / 2
        segments = segments[:i] + [gauss_kronrod(f, a, m, n)] + \
                   [gauss_kronrod(f, m, b, n)] + segments[i + 1:]

    if sum(e for (a, b, segint, e) in segments) > tol:
        print_nonconvergence_warning()
    return sum(segint for (a, b, segint, e) in segments)


def local_adaptive_gauss_kronrod(f, a, b, tol, maxiter, n=15):
    _, _, whole, err = gauss_kronrod(f, a, b, n)
    if not maxiter or err <= tol:
        return whole
    m = (a + b) / 2
    return local_adaptive_gauss_kronrod(f, a, m, tol / 2, maxiter - 1, n) + \
        local_adaptive_gauss_kronrod(f, m, b, tol / 2, maxiter - 1, n)
