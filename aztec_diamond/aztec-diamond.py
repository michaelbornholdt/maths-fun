"""Calculates domino tiling in an aztec Diamond.
This script tiles dominos in a random order into a aztec diamong. By doing so you can see the effects of the autec diamond theory. Refer to the readme for more details.

The tiling are saved in a dictionary with the coordinates as key and the state as values.
The state can be either "x" meaning no movemnt or it can be n,s,e or w for the four cardinal directions. If a tile is marked e = east, for example, it will move to the east in the next round of expansion, through the move() function.

The overall flow of the alg is: 
1. Initiate diamond of size 1 (with random initial directions)
2. Remove colliding blocks
3. Move the blocks to their new position in a larger diomond
4. Fill all gaps with random tiles
Repeat 2-4 until the wanted size is reached.

Example run from source:
'''python aztec_diamond\aztec-diamond.py'''

Returns:
    Saves file with results "out.html" to this folder.
"""

import numpy as np
import webbrowser


class aztecDiamond:
    """Class with all functions.
    class saves the current tiling in the self.tile variable.
    """

    def __init__(self, n):
        """intiatlize class and create a diamond of size n.

        Args:
            n ([int]): size of the aztec diamond.
        """
        assert type(n) == int, "init size must be integer"
        board = dict()
        for k in range(1, 2 * n + 1):
            l = min(2 * k, 4 * n - 2 * k + 2)
            for j in range(l):
                board[(j + 0.5 - l / 2, k - n - 0.5)] = "x"
        board[0] = n
        self.tile = board

    def removeBadBlocks(self):
        """Blocks which will collide in the coming move action will be removed here.

        Returns:
            tiles [dict]: the updated tile board.
        """
        bd = self.tile
        copy = dict(bd)  # to loop over all items, the 0 element needs to be removed.
        copy.pop(0)
        n = bd[0]
        for a, b in copy:
            try:
                # check for the two different kind of colliding blocks.
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
        """fills all "2x2" holes with two new tiles.

        Returns:
            tiles [dict]: board filled with new tiles. No holes anymore.
        """
        bd = self.tile
        n = bd[0]
        copy = dict(bd)  # create and pop the 0 element
        copy.pop(0)
        for a, b in copy:
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

    def move(self):
        """move all tiles in their indicated direction. In this step, the larger board is also initialized and then used from now onward.

        Returns:
            tiles [dict]: board with moved tiles.
        """
        bd = self.tile
        x = aztecDiamond(bd[0] + 1)
        board = x.tile
        copy = dict(bd)  # create and pop the 0 element
        copy.pop(0)
        for a, b in copy:
            if bd[(a, b)].lower() == "n":
                board[(a, b - 1)] = bd[(a, b)]
            if bd[(a, b)].lower() == "e":
                board[(a + 1, b)] = bd[(a, b)]
            if bd[(a, b)].lower() == "s":
                board[(a, b + 1)] = bd[(a, b)]
            if bd[(a, b)].lower() == "w":
                board[(a - 1, b)] = bd[(a, b)]
        return x

    def __str__(self):
        """make a string out of the dict to be able to print in command line.
        Example: print(str(bd))

        Returns:
            board [str]: string of diamond strcutrue
        """
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
        """Creates a html file out of the tiles which allows to have a visual representation of the dict.

        Args:
            out ([str]): name of the output file
        """
        ADpage = open(out, "w")
        n = self.tile[0]
        size = 500
        ADpage.write(
            f'<svg xmlns="http://www.w3.org/dx00/svg" width="{size}px" height="{size}px" version="1.1">\n'
        )
        dx = size / (2 * n + 1)
        center = size / 2
        copy = dict(self.tile)  # create and pop the 0 element
        copy.pop(0)
        for a, b in copy:
            direction = copy[a, b]
            x_pos = center + a * dx
            y_pos = center + b * dx
            if direction == "e":
                ADpage.write(
                    '<rect width="%s" height = "%s" x="%s" y="%s" style="fill:#3366FF" />\n'
                    % (dx, dx, x_pos, y_pos)
                )
            if direction == "w":
                ADpage.write(
                    '<rect width="%s" height = "%s" x="%s" y="%s" style="fill:orange" />\n'
                    % (dx, dx, x_pos, y_pos)
                )
            if direction == "n":
                ADpage.write(
                    '<rect width="%s" height = "%s" x="%s" y="%s" style="fill:#48ff00" />\n'
                    % (dx, dx, x_pos, y_pos)
                )
            if direction == "s":
                ADpage.write(
                    '<rect width="%s" height = "%s" x="%s" y="%s" style="fill:#CC0000" />\n'
                    % (dx, dx, x_pos, y_pos)
                )
        ADpage.write("</svg>")


def open_web(filename):
    """Opens the output file in the chrome webbrowser. When using, the registered location of the browser needs to be adapted.

    Args:
        filename ([type]): [description]
    """
    # adapt htis line for personal use.
    webbrowser.register(
        "chrome",
        None,
        webbrowser.BackgroundBrowser(
            "C://Program Files (x86)//Google//Chrome//Application//chrome.exe"
        ),
    )
    webbrowser.get("chrome").open(filename)


if __name__ == "__main__":
    """Executes the algorithm and ascs for the size of the aztec diamond."""
    bd = aztecDiamond(1).fillGoodBlocks()
    m = int(input("Aztec Diamond size? "))
    for x in range(m - 1):
        bd = bd.removeBadBlocks().move().fillGoodBlocks()
        if x == int(m / 2):
            print(f"Half way there! Your at n = {x} now")
    # print(str(bd))
    name = "aztec_diamond/out.html"
    bd.toSVG(name)
    open_web(name)
