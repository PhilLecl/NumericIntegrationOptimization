from itertools import chain, islice, cycle, repeat


def rectangle_rule(f, a, b, segcount):
    segwidth = (b - a) / segcount
    xs = (a + (i + 0.5) * segwidth for i in range(segcount))
    area = sum(f(xi) for xi in xs) * segwidth
    return area


def trapezoidal_rule(f, a, b, segcount):
    segwidth = (b - a) / segcount
    xs = (a + i * segwidth for i in range(segcount + 1))
    ws = chain([1], repeat(2, segcount - 1), [1])
    area = sum(f(xi) * wi for xi, wi in zip(xs, ws)) * segwidth / 2
    return area


def simpsons_rule(f, a, b, segcount):
    segcount *= 2
    h = (b - a) / segcount
    xs = (a + i * h for i in range(segcount + 1))
    ws = chain([1], islice(cycle([4, 2]), segcount - 1), [1])
    area = sum(f(xi) * wi for xi, wi in zip(xs, ws)) * h / 3
    return area


def booles_rule(f, a, b, segcount):
    segcount *= 4
    h = (b - a) / segcount
    xs = (a + i * h for i in range(segcount + 1))
    ws = chain([7], islice(cycle([32, 12, 32, 14]), segcount - 1), [7])
    area = sum(f(xi) * wi for xi, wi in zip(xs, ws)) * h * 2 / 45
    return area
