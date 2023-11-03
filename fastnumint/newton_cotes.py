from itertools import chain, islice, cycle, repeat
from .util import basic_iter, orderab


@orderab
@basic_iter()
def rectangle_rule(f, a, b, segcount):
    segwidth = (b - a) / segcount
    xs = (a + (i + 0.5) * segwidth for i in range(segcount))
    area = sum(f(xi) for xi in xs) * segwidth
    return area


@orderab
@basic_iter()
def trapezoidal_rule(f, a, b, segcount):
    segwidth = (b - a) / segcount
    xs = (a + i * segwidth for i in range(segcount + 1))
    ws = chain([1], repeat(2, segcount - 1), [1])
    area = sum(f(xi) * wi for xi, wi in zip(xs, ws)) * segwidth / 2
    return area


@orderab
@basic_iter()
def simpsons_rule(f, a, b, segcount):
    segcount *= 2
    h = (b - a) / segcount
    xs = (a + i * h for i in range(segcount + 1))
    ws = chain([1], islice(cycle([4, 2]), segcount - 1), [1])
    area = sum(f(xi) * wi for xi, wi in zip(xs, ws)) * h / 3
    return area


@orderab
@basic_iter()
def booles_rule(f, a, b, segcount):
    segcount *= 4
    h = (b - a) / segcount
    xs = (a + i * h for i in range(segcount + 1))
    ws = chain([7], islice(cycle([32, 12, 32, 14]), segcount - 1), [7])
    area = sum(f(xi) * wi for xi, wi in zip(xs, ws)) * h * 2 / 45
    return area


def _simpson(f, a, fa, b, fb):
    m = (a + b) / 2
    fm = f(m)
    return m, fm, (fa + 4 * fm + fb) * (b - a) / 6


def _asr(f, a, fa, m, fm, b, fb, whole, tol, maxdepth):
    if maxdepth <= 0:
        return whole
    lm, flm, left = _simpson(f, a, fa, m, fm)
    rm, frm, right = _simpson(f, m, fm, b, fb)
    delta = (left + right - whole) / 15
    if abs(delta) <= tol:
        return left + right + delta
    return _asr(f, a, fa, lm, flm, m, fm, left, tol / 2, maxdepth - 1) + \
        _asr(f, m, fm, rm, frm, b, fb, right, tol / 2, maxdepth - 1)


@orderab
def local_adaptive_simpsons_rule(f, a, b, tol, maxdepth):
    fa, fb = f(a), f(b)
    m, fm, whole = _simpson(f, a, fa, b, fb)
    return _asr(f, a, fa, m, fm, b, fb, whole, tol, maxdepth - 1)
