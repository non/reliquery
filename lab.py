class Labyrinth(object):
    #w = 19
    #h = 19
    #scale = 20
    w = 3
    h = 3
    scale = 1 #20
    imgw = w * scale
    imgh = h * scale

    tiles = {
        '#': [[0 for x in xrange(scale)] for y in xrange(scale)],
        '.': [[0xff for x in xrange(scale)] for y in xrange(scale)],
    }

    @classmethod
    def render(cls, rows):
        pixels = [0xff for i in xrange(cls.imgw * cls.imgh)]
        for y, row in enumerate(rows):
            for x, sym in enumerate(row):
                tile = cls.tiles[sym]
                print x, y, sym, tile
                for iy in xrange(0, cls.scale):
                    ny = ((y * cls.scale) + iy) * cls.imgw
                    for ix in xrange(0, cls.scale):
                        nx = (x * cls.scale + ix)
                        pixels[ny + nx] = tile[iy][ix]
        return pixels

    test = ['###', '#.#', '###']

print Labyrinth.render(Labyrinth.test)
