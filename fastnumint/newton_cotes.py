def _rectangle_rule(f, a, b, segcount):
    segwidth = (b - a) / segcount
    xs = [a + (i + 0.5) * segwidth for i in range(segcount)]
    area = sum(f(xs[i]) for i in range(segcount)) * segwidth
    return area


def _trapezoidal_rule(f, a, b, segcount):
    segwidth = (b - a) / segcount
    xs = [a + i * segwidth for i in range(segcount + 1)]
    area = sum((f(xs[i]) + f(xs[i + 1])) for i in range(segcount)) * segwidth / 2
    return area


def _simpsons_rule(f, a, b, segcount):
    segcount *= 2
    h = (b - a) / segcount
    xs = [a + i * h for i in range(segcount + 1)]
    area = sum((f(xs[i + 0]) + 4 * f(xs[i + 1]) + f(xs[i + 2])) for i in
               range(0, segcount, 2)) * h / 3
    return area


def _booles_rule(f, a, b, segcount):
    segcount *= 4
    h = (b - a) / segcount
    xs = [a + i * h for i in range(segcount + 1)]
    area = sum((7 * f(xs[i]) + 32 * f(xs[i + 1]) + 12 * f(xs[i + 2]) + 32 * f(xs[i + 3]) +
                7 * f(xs[i + 4])) for i in range(0, segcount, 4)) * h * 2 / 45
    return area