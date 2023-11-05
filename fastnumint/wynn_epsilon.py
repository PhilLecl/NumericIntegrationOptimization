class WynnEpsilon:
    def __init__(self):
        self.table = []  # list of rows, initially empty

    @property
    def n(self):
        return len(self.table)

    @property
    def extrapolation(self):
        n = self.n
        m = (n - 1) % 2
        return self.table[m][n - m]

    def add(self, partial_sum):
        self.table.append([0, partial_sum])
        n = self.n
        for i in range(1, n):
            row = n - i - 1
            col = 1 + i
            self.table[row].append(self.table[row + 1][col - 2] + 1 / (
                    self.table[row + 1][col - 1] - self.table[row][col - 1]))


if __name__ == '__main__':
    s = 0
    wynn = WynnEpsilon()
    for k in range(0, 14):
        s += 4 * (-1) ** k / (2 * k + 1)
        wynn.add(s)
        print(s, wynn.extrapolation)
