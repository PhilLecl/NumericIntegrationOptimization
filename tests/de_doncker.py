import math


# region ws
def w1(x, alpha, beta):
    return x ** beta + (1 - x) ** alpha


def w2(x, alpha, beta):
    return w1(x, alpha, beta) * math.log(x)


def w3(x, alpha, beta):
    return w1(x, alpha, beta) * math.log(1 - x)


def w4(x, alpha, beta):
    return w1(x, alpha, beta) * math.log(x) * math.log(1 - x)


ws = (w1, w2, w3, w4)
# endregion

# region fs
f1 = math.exp


def f2(x):
    return 1 / (1 + math.exp(x))


def f3(x):
    return 1 / (1 + x ** 2)


def f4(x):
    return 1 / (1 + x ** 4)


f5 = math.cos


def f6(x):
    return x ** (3 / 2)


def f7(x):
    return math.sqrt(abs(x ** 2 - 0.25))


# endregion


_a, _b, _tol = 1e-6, 1 - 1e-6, 1e-8
TEST_CASES = (('f', 'w', 'alpha', 'beta', 'a', 'b', 'tol', 'maxiter'),
              [(f1, w, -0.5, -0.5, _a, _b, _tol, 1000) for w in ws] + \
              [(f2, w, -0.5, -0.5, _a, _b, _tol, 1000) for w in ws] + \
              [(f3, w, -1 / 3, -0.5, _a, _b, _tol, 1000) for w in ws] + \
              [(f4, w, -1 / 3, -0.5, _a, _b, _tol, 1000) for w in ws] + \
              [(f5, w, -1 / 3, -1 / 3, _a, _b, _tol, 1000) for w in ws] + \
              [(f6, w, 0.5, -1 / 3, _a, _b, _tol, 1000) for w in ws] + \
              [(f7, w, -0.5, -1 / 3, _a, _b, _tol, 1000) for w in ws])
