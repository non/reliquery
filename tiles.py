from os.path import dirname, join, realpath
from PIL import Image

base = dirname(realpath(__file__))

db = {}

def load(path, size):
    if path not in db:
        db[path] = loadtiles(path, size)
    return db[path]

def loadtiles(name, size):
    path = join(base, name)
    img = Image.open(path)
    x0, y0, x1, y1 = img.getbbox()
    dx = x1 - x0
    dy = y1 - y0
    assert dx % size == 0, dy % size == 0
    tiles = []
    for y in range(y0, y1, size):
        for x in range(x0, x1, size):
            tile = img.crop((x, y, x + size, y + size)).convert('1')
            tiles.append(tile)
    return img, tiles
