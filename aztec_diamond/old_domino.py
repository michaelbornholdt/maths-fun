import numpy as np


class aztecDiamond:
    def __init__(self, x):
        if type(x) == type(0):
            n = x
            board = dict()
            for k in range(1, 2 * n + 1):
                l = min(2 * k, 4 * n - 2 * k + 2)
                for j in range(l):
                    board[(j + 0.5 - l / 2, k - n - 0.5)] = "x"
            board[0] = n
            self.tile = board
        elif type(x) == type(""):
            b = x
            sq = b.split("\n")
            board = dict()
            n = int(len(sq) / 2)
            for k in range(1, 2 * n + 1):
                l = min(2 * k, 4 * n - 2 * k + 2)
                row = sq[k - 1].replace(".", "")
                for j in range(l):
                    board[(j + 0.5 - l / 2, k - n - 0.5)] = row[j]
            board[0] = len(sq) / 2
            self.tile = board

    def removeBadBlocks(self):
        bd = self.tile
        n = bd[0]
        for k in range(1, 2 * n + 1):
            l = min(2 * k, 4 * n - 2 * k + 2)
            for j in range(l):
                a, b = j + 0.5 - l / 2, k - n - 0.5
                try:
                    if (
                        bd[(a, b)].lower() == "s"
                        and bd[(a + 1, b)].lower() == "s"
                        and bd[(a, b + 1)].lower() == "n"
                        and bd[(a + 1, b + 1)].lower() == "n"
                    ) or (
                        bd[(a, b)].lower() == "e"
                        and bd[(a + 1, b)].lower() == "w"
                        and bd[(a, b + 1)].lower() == "e"
                        and bd[(a + 1, b + 1)].lower() == "w"
                    ):
                        bd[(a, b)] = "x"
                        bd[(a + 1, b)] = "x"
                        bd[(a, b + 1)] = "x"
                        bd[(a + 1, b + 1)] = "x"
                except:
                    pass
        self.tile = bd
        return self

    def fillGoodBlocks(self):
        bd = self.tile
        n = bd[0]
        for k in range(1, 2 * n + 1 - 1):
            l = min(2 * k, 4 * n - 2 * k + 2)
            for j in range(l - 1):
                a, b = j + 0.5 - l / 2, k - n - 0.5
                try:
                    if (
                        bd[(a, b)] == "x"
                        and bd[(a + 1, b)] == "x"
                        and bd[(a, b + 1)] == "x"
                        and bd[(a + 1, b + 1)] == "x"
                    ):
                        if np.random.rand() > 0.5:
                            bd[(a, b)] = "n"
                            bd[(a + 1, b)] = "n"
                            bd[(a, b + 1)] = "s"
                            bd[(a + 1, b + 1)] = "s"
                        else:
                            bd[(a, b)] = "w"
                            bd[(a + 1, b)] = "e"
                            bd[(a, b + 1)] = "w"
                            bd[(a + 1, b + 1)] = "e"
                except:
                    pass
        self.tile = bd
        return self

    def shuffle(self):
        bd = self.tile
        x = aztecDiamond(bd[0] + 1)
        board = x.tile
        n = bd[0]
        for k in range(1, 2 * n + 1):
            l = min(2 * k, 4 * n - 2 * k + 2)
            for j in range(l):
                if bd[(j + 0.5 - l / 2, k - n - 0.5)].lower() == "n":
                    board[(j + 0.5 - l / 2, k - n - 0.5 - 1)] = bd[
                        (j + 0.5 - l / 2, k - n - 0.5)
                    ]
                if bd[(j + 0.5 - l / 2, k - n - 0.5)].lower() == "e":
                    board[(j + 0.5 - l / 2 + 1, k - n - 0.5)] = bd[
                        (j + 0.5 - l / 2, k - n - 0.5)
                    ]
                if bd[(j + 0.5 - l / 2, k - n - 0.5)].lower() == "s":
                    board[(j + 0.5 - l / 2, k - n - 0.5 + 1)] = bd[
                        (j + 0.5 - l / 2, k - n - 0.5)
                    ]
                if bd[(j + 0.5 - l / 2, k - n - 0.5)].lower() == "w":
                    board[(j + 0.5 - l / 2 - 1, k - n - 0.5)] = bd[
                        (j + 0.5 - l / 2, k - n - 0.5)
                    ]
        return x

    def __str__(self):
        bd = self.tile
        n = bd[0]
        s = ""
        for k in range(1, 2 * n + 1):
            l = min(2 * k, 4 * n - 2 * k + 2)
            s += (
                (int((2 * n - l) / 2) * ".")
                + "".join([bd[(j + 0.5 - l / 2, k - n - 0.5)] for j in range(l)])
                + (int((2 * n - l) / 2) * ".")
                + "\n"
            )
        return s.replace("x", " ")

    def toSVG(self, out):
        ADpage = open(out, "w")
        n = self.tile[0]
        size = n * 30
        ADpage.write(
            f'<svg xmlns="http://www.w3.org/dx00/svg" width="{size}px" height="{size}px" version="1.1">\n'
        )
        w = 1
        color = "black"
        dx = 10
        for k in range(1, 2 * n + 1):
            l = min(2 * k, 4 * n - 2 * k + 2)
            c = 0
            for x in (
                ["." for j in range(int((2 * n - l) / 2))]
                + [self.tile[(j + 0.5 - l / 2, k - n - 0.5)] for j in range(l)]
                + ["." for j in range(int((2 * n - l) / 2))]
            ):
                if x == "e":
                    ADpage.write(
                        '<rect width="%s" height = "%s" x="%s" y="%s" style="fill:#3366FF" />\n'
                        % (dx, dx, c, dx * k)
                    )
                if x == "w":
                    ADpage.write(
                        '<rect width="%s" height = "%s" x="%s" y="%s" style="fill:orange" />\n'
                        % (dx, dx, c, dx * k)
                    )
                if x == "n":
                    ADpage.write(
                        '<rect width="%s" height = "%s" x="%s" y="%s" style="fill:greenyellow" />\n'
                        % (dx, dx, c, dx * k)
                    )
                if x == "s":
                    ADpage.write(
                        '<rect width="%s" height = "%s" x="%s" y="%s" style="fill:#CC0000" />\n'
                        % (dx, dx, c, dx * k)
                    )
                c += dx
        ADpage.write("</svg>")


if __name__ == "__main__":
    bd = aztecDiamond(1).fillGoodBlocks()
    # bd = aztecDiamond(file('in.txt').read())

    m = int(input("Aztec Diamond size? "))
    # m = 10
    for x in range(m - 1):
        bd = bd.removeBadBlocks().shuffle().fillGoodBlocks()
    print(str(bd))
    bd.toSVG("out.html")
