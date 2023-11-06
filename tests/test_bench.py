import pytest
from scipy import integrate
from fastnumint import int_num
from tests.functions import *
from .de_doncker import TEST_CASES as DE_DONCKER_TESTS

MY_TESTS = (('f', 'a', 'b', 'tol', 'maxiter'), (
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
    (logistic, -2, 2, 1e-8, 1000),
    (logistic, -5, 5, 1e-8, 1000),
    (logistic, -10, 10, 1e-8, 1000),
    (p0, -1, 1, 1e-8, 1000),
    (p1, -1, 1, 1e-8, 1000),
    (p2, -1, 1, 1e-8, 1000),
    (p3, -1, 1, 1e-8, 1000),
    (p4, -1, 1, 1e-8, 1000),
    (p0, 0, -4, 1e-8, 1000),
    (p1, 0, -4, 1e-8, 1000),
    (p2, 0, -4, 1e-8, 1000),
    (p3, 0, -4, 1e-8, 1000),
    (p4, 0, -4, 1e-8, 1000),
))


def test_original(benchmark):
    """The test case originially supplied in the class"""
    f, a, b, tol, maxiter = psi_harm, -5, 5, 1e-8, 1000
    my_result = benchmark(int_num, f, a, b, tol, maxiter)
    scipy_result = integrate.quad(f, a, b)
    assert abs(my_result - scipy_result[0]) <= tol


@pytest.mark.parametrize(*MY_TESTS)
def test_custom(benchmark, f, a, b, tol, maxiter):
    """A couple of test cases I made up"""
    my_result = benchmark(int_num, f, a, b, tol, maxiter)
    scipy_result = integrate.quad(f, a, b)
    assert abs(my_result - scipy_result[0]) <= tol


def test_tan(benchmark):
    """Tangens as a separate test case because some algorithms struggle with it."""
    f, a, b, tol, maxiter = math.tan, -math.pi, math.pi, 1e-8, 1000
    my_result = benchmark(int_num, f, a, b, tol, maxiter)
    solution = 0
    assert abs(my_result - solution) <= tol


@pytest.mark.parametrize(('f', 'a', 'b', 'tol', 'maxiter'), (
        (p50, -1, 1, 1e-8, 1000),
        (p50, 0, -1, 1e-8, 1000)
))
def test_p50(benchmark, f, a, b, tol, maxiter):
    """Polynomial of degree 50 as edge case because it's a rare application."""
    my_result = benchmark(int_num, f, a, b, tol, maxiter)
    scipy_result = integrate.quad(f, a, b)
    assert abs(my_result - scipy_result[0]) <= tol


@pytest.mark.parametrize(*DE_DONCKER_TESTS)
def test_de_doncker(benchmark, f, w, alpha, beta, a, b, tol, maxiter):
    """Test cases from [de Doncker 1978] (https://doi.org/10.1145/1053402.1053403)"""
    fw = lambda x: f(x) * w(x, alpha, beta)
    my_result = benchmark(int_num, fw, a, b, tol, maxiter)
    scipy_result = integrate.quad(fw, a, b, limit=1000)
    assert abs(my_result - scipy_result[0]) <= tol


@pytest.mark.skip(reason='Too difficult')
def test_challenging():
    """Test case from [Gautschi 2008] (https://doi.org/10.1007/s11075-008-9157-z)."""
    f = lambda x: math.cos(math.log(x) / x) / x
    a, b, tol, maxiter = 0, 1, 1e-8, 10 ** 5
    my_result = int_num(f, a, b, tol, maxiter)
    solution = 0.323367431677778761399370087952170446651046625725469661681036443
    assert abs(my_result - solution) <= tol
