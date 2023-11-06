import math


class WynnEpsilon:
    def __init__(self):
        self.table = []  # list of rows, initially empty
        self._extrapolations = []

    @property
    def n(self):
        return len(self.table)

    @property
    def extrapolation(self):
        return self._extrapolations[-1] if self._extrapolations else float('inf')

    @property
    def error(self):
        return abs(self._extrapolations[-1] - self._extrapolations[-4]) \
            if self.n >= 4 else float('inf')

    def _update_extrapolations(self):
        n = self.n
        m = (n - 1) % 2
        self._extrapolations.append(self.table[m][n - m])

    def add(self, partial_sum):
        self.table.append([0, partial_sum])
        n = self.n
        for i in range(1, n):
            row = n - i - 1
            col = 1 + i
            self.table[row].append(self.table[row + 1][col - 2] + 1 / (
                    self.table[row + 1][col - 1] - self.table[row][col - 1]))
        self._update_extrapolations()


if __name__ == '__main__':  # for debugging purposes
    s = 0
    wynn = WynnEpsilon()
    for k in range(0, 22):
        s += 4 * (-1) ** k / (2 * k + 1)
        wynn.add(s)
        print(k, s, wynn.extrapolation, wynn.error)
        assert abs(math.pi - wynn.extrapolation) < wynn.error
