import pytest
import math
from scipy import integrate
from fastnumint import int_num, int_num_cachedf
from tests.functions import psi_harm, psi_harm_sq, pyexp

TEST_CASES = (('f', 'a', 'b', 'tol', 'maxiter'), [
    (psi_harm, -5, 5, 1e-8, 1000),
    (psi_harm, 5, -5, 1e-8, 1000),
    (psi_harm_sq, -1, 1, 1e-8, 1000),
    (psi_harm_sq, -2, 2, 1e-8, 1000),
    (psi_harm_sq, -5, 5, 1e-4, 1000),
    (psi_harm_sq, -5, 5, 1e-6, 1000),
    (psi_harm_sq, -5, 5, 1e-8, 1000),
    (psi_harm_sq, -5, 5, 1e-10, 1000),
    (psi_harm_sq, -10, 10, 1e-8, 1000),
    (math.exp, 0, -10, 1e-8, 1000),
    (math.exp, 0, 10, 1e-8, 1000),
    (math.exp, -10, 10, 1e-4, 1000),
    (pyexp, 0, 10, 1e-8, 1000),
    (math.sin, 0, math.pi, 1e-8, 1000),
    (math.cos, 0, math.pi, 1e-8, 1000),
    (math.sin, 0, 2 * math.pi, 1e-8, 1000),
    (math.cos, 0, 2 * math.pi, 1e-8, 1000),
])


@pytest.mark.parametrize(*TEST_CASES)
def test_int_num(benchmark, f, a, b, tol, maxiter):
    my_result = benchmark(int_num, f, a, b, tol, maxiter)
    scipy_result = integrate.quad(f, a, b)
    assert abs(my_result - scipy_result[0]) <= tol


@pytest.mark.parametrize(*TEST_CASES)
def test_cached(benchmark, f, a, b, tol, maxiter):
    benchmark(int_num_cachedf, f, a, b, tol, maxiter)
