from scipy import special
import math
import numpy as np


def psi_harm(x, n=5):
    H = special.hermite(n)
    C = (1 / (np.pi)) ** (0.25) * 1 / (2 ** n * math.factorial(n)) ** (0.5)
    res = C * H(x) * np.exp(-x ** 2 / 2)
    return res


def psi_harm_sq(x, n=5):
    return psi_harm(x, n) ** 2


def pyexp(x):
    return math.e**x
