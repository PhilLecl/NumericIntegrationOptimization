import pytest
import math
from src.int_num import int_num
from tests.functions import psi_harm_sq


def test_phs_rough(benchmark):
    benchmark(int_num, psi_harm_sq, -5, 5, 1e-4, 1000)


def test_phs(benchmark):
    benchmark(int_num, psi_harm_sq, -5, 5, 1e-8, 1000)


def test_phs_precise(benchmark):
    benchmark(int_num, psi_harm_sq, -5, 5, 1e-10, 1000)


def test_exp(benchmark):
    benchmark(int_num, math.exp, -2.5, 2.5, 1e-4, 1000)


def test_exp2(benchmark):
    benchmark(int_num, math.exp, 0, -5, 1e-8, 1000)
