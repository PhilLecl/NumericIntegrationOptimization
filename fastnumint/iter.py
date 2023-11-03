def print_nonconvergence_warning():
    print('----------------------------------')
    print('   WARNING: maxiter was reached   ')
    print('Your calculation did not converge!')
    print('----------------------------------')
    print()


def basic_iter(calc_area, init_segcount=4):
    def wrapper(f, a, b, tol, maxiter):
        segcount = init_segcount
        area = calc_area(f, a, b, segcount)
        for _ in range(maxiter):
            old_area = area
            segcount *= 2
            area = calc_area(f, a, b, segcount)
            if abs(area - old_area) <= tol:
                return area
        print_nonconvergence_warning()
        return area

    return wrapper


def composite_iter(calc_area, init_segcount=1):
    def wrapper(f, a, b, tol, maxiter):
        segcount = init_segcount
        area = _composite(calc_area, segcount)(f, a, b)
        for _ in range(maxiter):
            old_area = area
            segcount *= 2
            area = _composite(calc_area, segcount)(f, a, b)
            if abs(area - old_area) <= tol:
                return area
        print_nonconvergence_warning()
        return area

    return wrapper


def _composite(calc_area, segcount):
    def wrapper(f, a, b):
        h = (b - a) / segcount
        xs = [a + i * h for i in range(segcount + 1)]
        return sum(calc_area(f, xs[i], xs[i + 1]) for i in range(segcount))

    return wrapper
