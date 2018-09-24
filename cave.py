import network
from itertools import permutations
from PIL import Image
from random import choice, random, randint, shuffle

class Map(object):

    cardinal = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    allcardinals = list(permutations(cardinal))

    adjacent = [
        (-1, -1), (-1, +0), (-1, +1),
        (+0, -1),           (+0, +1),
        (+1, -1), (+1, +0), (+1, +1)
    ]

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [['#' for i in range(width)] for j in range(height)]

    @classmethod
    def randomcardinal(cls):
        return choice(cls.allcardinals)

    @classmethod
    def maze_init(cls, w, h):
        maze = Map(w, h)
        for x in range(1, w - 1, 2):
            for y in range(1, h - 1, 2):
                maze.set(x, y, '.')
        return maze

    @classmethod
    def maze_backtrack(cls, w, h, ds=[(2, 0), (0, 2), (-2, 0), (0, -2)]):
        maze = cls.maze_init(w, h)
        ds = list(ds)
        seen = set()
        def in_bounds(x, y):
            return 0 < x and x < (w - 1) and 0 < y and y < (h - 1)
        def recur(x0, y0):
            if (x0, y0) in seen:
                return
            seen.add((x0, y0))
            shuffle(ds)
            for dx, dy in ds:
                x1, y1 = x0 + dx, y0 + dy
                if in_bounds(x1, y1) and (x1, y1) not in seen:
                    maze.set(x0 + (dx / 2), y0 + (dy / 2), '.')
                    recur(x1, y1)
        recur(1, 1)
        maze.set(1, 0, '.')
        maze.set(-2, -1, '.')
        return maze

    @classmethod
    def maze_kruskal(cls, w, h):
        maze = Map(w, h)
        walls = []
        for x in range(2, w - 1, 2):
            for y in range(1, h - 1, 2):
                walls.append((x, y))
        for x in range(1, w - 1, 2):
            for y in range(2, h - 1, 2):
                walls.append((x, y))
        cells = {}
        colors = 0
        for x in range(1, w - 1, 2):
            for y in range(1, h - 1, 2):
                cells[(x, y)] = colors
                maze.set(x, y, '.')
                colors += 1
        shuffle(walls)
        for (wx, wy) in walls:
            if (wx % 2) == 0:
                sx0, sx1 = wx - 1, wx + 1
                sy0, sy1 = wy, wy
            else:
                sx0, sx1 = wx, wx
                sy0, sy1 = wy - 1, wy + 1
            c0 = cells[(sx0, sy0)]
            c1 = cells[(sx1, sy1)]
            if c0 != c1:
                maze.set(wx, wy, '.')
                for k in cells:
                    if cells[k] == c1:
                        cells[k] = c0
        maze.set(1, 0, '.')
        maze.set(-2, -1, '.')
        return maze

    def isvalid(self, x, y):
        return 0 <= x and x < self.width and 0 <= y and y < self.height

    def isopen(self, x, y):
        return self.grid[y][x] == '.'

    def iswall(self, x, y):
        return self.grid[y][x] == '#'

    def get(self, x, y):
        return self.grid[y][x]

    def set(self, x, y, glyph):
        self.grid[y][x] = glyph

    def render(self, scale, glyphs, tiles0):
        tiles = [t.resize((scale, scale)) for t in tiles0]
        canvas = Image.new('1', (self.width * scale, self.height * scale))
        for row in range(0, self.height):
            for col in range(0, self.width):
                tile = tiles[glyphs[self.grid[row][col]]]
                canvas.paste(tile, (col * scale, row * scale))
        return canvas
