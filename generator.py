import network
from itertools import permutations
from PIL import Image
from subprocess import call
from random import choice, random, randint, shuffle
import re
import sys
import tiles

from cave import Map

vowels = set('aeiouy')

def a_an(noun):
    if noun and noun[0] in vowels:
        return 'an'
    else:
        return 'a'

class Generator(object):
    name = None
    @classmethod
    def generate(cls, p):
        p.println('unimplemented %r' % cls)

class Diagnostic(Generator):
    name = 'diagnostic'
    cls_re = re.compile(r"^<class '.+\.([^.]+)'>$")
    @classmethod
    def generate(cls, r):
        r.println('reliquery diagnostic')
        r.println('ip: %s' % r.ip)
        r.println('generators:')
        for i, g in enumerate(r.generators):
            s = str(g)[:32]
            m = cls.cls_re.match(str(g))
            if m:
                s = m.group(1)
            r.println("%d: %s" % (i + 1, s))

class Magic8(Generator):
    name = 'magic8'
    responses = [
        "it is certain",
        "it is decidedly so",
        "without a doubt",
        "yes definitely",
        "you may rely on it",
        "as i see it, yes",
        "most likely",
        "outlook good",
        "yes",
        "signs point to yes",
        "reply hazy try again",
        "ask again later",
        "better not tell you now",
        "cannot predict now",
        "concentrate and ask again",
        "don't count on it",
        "my reply is no",
        "my sources say no",
        "outlook not so good",
        "very doubtful"
    ]

    @classmethod
    def generate(cls, p):
        p.println('magic 8-ball says:')
        p.println('  "%s"' % choice(cls.responses))

class Tarot(Generator):
    name = 'tarot'
    majors = [
        "the fool",
        "the magician",
        "the high priestess",
        "the empress",
        "the emperor",
        "the hierophant",
        "the lovers",
        "the chariot",
        "justice",
        "the hermit",
        "wheel of fortune",
        "strength",
        "the hanged man",
        "death",
        "temperance",
        "the devil",
        "the tower",
        "the star",
        "the moon",
        "the sun",
        "judgement",
        "the world",
    ]
    suits = [
        'cups',
        'wands',
        'swords',
        'pentacles',
    ]
    ranks = [
        "ace",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
        "ten",
        "page",
        "knight",
        "queen",
        "king",
    ]
    cards = []
    for m in majors:
        cards.append(m)
    for s in suits:
        for r in ranks:
            cards.append('%s of %s' % (r, s))

    @classmethod
    def generate(cls, p):
        card = choice(cls.cards)
        # need to ensure printed line <= 32
        p.println('tarot: %s' % card)


class Potion(Generator):
    name = 'potion'
    tints = {
        'metallic': ['brassy', 'bronze', 'coppery', 'gold', 'silvery', 'steely'],
        'white': ['bone', 'colorless', 'ivory', 'pearl'],
        'gray': ['dove', 'dun', 'neutral'],
        'brown': ['chocolate', 'ecru', 'fawn', 'mahogany', 'tan', 'terra cotta'],
        'black': ['ebony', 'inky', 'pitchy', 'sable', 'sooty'],
        'violet': ['fuchsia', 'heliotrope', 'lake', 'lavender', 'lilac', 'magenta', 'mauve', 'plum', 'puce', 'purple'],
        'yellow': ['amber', 'buff', 'citrine', 'cream', 'fallow', 'flaxen', 'ochre', 'peach', 'saffron', 'straw'],
        'red': ['carmine', 'cerise', 'cherry', 'cinnabar', 'coral', 'crimson', 'madder', 'maroon', 'pink', 'rose', 'ruby', 'russet', 'rust', 'sanguine', 'scarlet', 'vermillion'],
        'green': ['aquamarine', 'emerald', 'olive'],
        'blue': ['azure', 'cerulean', 'indigo', 'sapphire', 'turquoise', 'ultramarine'],
        'orange': ['apricot', 'flame', 'golden', 'salmon', 'tawny'],
    }
    colors = list(tints.keys())
    appearances = ['bubbling', 'cloudy', 'effervescent', 'fuming', 'oily', 'smoky', 'syrupy', 'vaporous', 'viscous', 'watery']
    consistencies = ['clear', 'flecked', 'layered', 'luminous', 'opaline', 'phosphorescent', 'rainbowed', 'ribboned', 'translucent', 'variegated']
    tastes = ['acidic', 'bilious', 'bitter', 'burning', 'buttery', 'dusty', 'earthy', 'fiery', 'fishy', 'greasy', 'herbal', 'honeyed', 'lemony', 'meaty', 'metallic', 'milky', 'musty', 'oniony', 'peppery', 'perfumy', 'salty', 'soothing', 'sour', 'spicy', 'sweet', 'tart', 'vinegary', 'watery']

    @classmethod
    def generate(cls, p):
        color = choice(cls.colors)
        tint = choice(cls.tints[color])
        consistency = choice(cls.consistencies)
        taste = choice(cls.tastes)
        p.println('%s %s %s potion' % (a_an(consistency), consistency, color))
        p.println('  it has %s %s tint' % (a_an(tint), tint))
        p.println('  and %s %s flavor' % (a_an(taste), taste))

class Labyrinth(Generator):
    name = 'labyrinth'
    glyphs = {
        '#': 0,
        '.': 13,
    }

    @classmethod
    def generate(cls, p):
        scale = 8 if p.switch.is_pressed else 16
        w = (384 / scale) - 1
        h = (384 / scale) - 1
        fs = [
            lambda w, h: Map.maze_backtrack(w, h, ds=[(2, 0), (2, 0), (0, 2), (-2, 0), (-2, 0), (0, -2)]),
            lambda w, h: Map.maze_backtrack(w, h, ds=[(2, 0), (0, 2), (0, 2), (-2, 0), (0, -2), (0, -2)]),
            lambda w, h: Map.maze_backtrack(w, h, ds),
            lambda w, h: Map.maze_kruskal(w, h),
        ]
        maze = choice(fs)(w, h)
        _, ptiles = tiles.load('16tiles.bmp', 16)
        canvas = maze.render(scale, cls.glyphs, ptiles)
        p.println('enter the labyrinth!')
        p.printImage(canvas, True)

class Tiles(Generator):
    name = 'tiles'
    @classmethod
    def generate(cls, p):
        scale = 8 if p.switch.is_pressed else 16
        canvas = Image.new('1', (384, 384))
        def r():
            return choice(p.tiles).resize((scale, scale))
        for y in range(0, 384, scale):
            for x in range(0, 384, scale):
                canvas.paste(r(), (x, y))
        p.printImage(canvas, True)

import names

class Npc(Generator):
    name = 'npc'

    alignments = [
        'Lawful-Good', 'Neutral-Good', 'Chaotic-Good',
        'Neutral-Good', 'True-Neutral', 'Chaotic-Neutral',
        'Lawful-Evil', 'Neutral-Evil', 'Chaotic-Evil',
    ]

    races = [
        ('Human', [], []),
        ('Half-elf', [], []),
        ('Half-orc', ['str'], ['int', 'cha']),
        ('Elf', ['dex'], ['con']),
        ('Dwarf', ['con'], ['cha']),
        ('Gnome', ['int'], ['wis']),
        ('Halfling', ['dex'], ['str']),
    ]

    professions = [
        ('Barbarian', 'str'),
        ('Fighter', 'str'),
        ('Ranger', 'str'),
        ('Paladin', 'str'),
        ('Cleric', 'wis'),
        ('Druid', 'wis'),
        ('Wizard', 'int'),
        ('Sorcerer', 'int'),
        ('Thief', 'dex'),
        ('Bard', 'dex'),
        ('Monk', 'dex'),
    ]

    stats = ['str', 'int', 'wis', 'dex', 'con', 'cha']

    @classmethod
    def generate(cls, p):

        def swap(stats, goalk):
            best = None
            for k in stats:
                if best is None or stats[k] > best[1]:
                    best = (k, stats[k])
            maxk, maxv = best
            if maxk != goalk:
                temp = stats[maxk]
                stats[maxk] = stats[goalk]
                stats[goalk] = temp

        def roll(num, sides):
            total = 0
            for i in range(0, num):
                total += randint(1, sides)
            return total

        mfn = 'M' if random() < 0.5 else 'F'

        name = names.createname(mfn)
        alignment = choice(cls.alignments)
        race, inc, dec = choice(cls.races)
        profession, profstat = choice(cls.professions)
        stats = dict([(s, roll(3, 6)) for s in cls.stats])

        traits = names.choosetraits(3)

        swap(stats, profstat)

        for s in inc:
            stats[s] += 1
        for s in dec:
            stats[s] -= 1

        p.println(name)
        p.println('%s %s %s' % (alignment, race, profession))
        p.println('STR %2d    INT %2d' % (stats['str'], stats['int']))
        p.println('DEX %2d    WIS %2d' % (stats['dex'], stats['wis']))
        p.println('CON %2d    CHA %2d' % (stats['con'], stats['cha']))
        p.println('Traits:')
        for t in traits:
            p.println(' - %s' % t)

class Cave(Generator):
    name = 'cave'
    glyphs = {
        '#': 0,
        '.': 13,
    }

    cardinal = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    allcardinals = list(permutations(cardinal))

    @classmethod
    def randomcardinal(cls):
        return choice(cls.allcardinals)

    adjacent = [
        (-1, -1), (-1, +0), (-1, +1),
        (+0, -1),           (+0, +1),
        (+1, -1), (+1, +0), (+1, +1)
    ]

    @classmethod
    def init(cls, w, h):
        attempts = 10
        for i in range(0, attempts):
            cave = Map(w, h)
            for x in range(1, w - 1):
                for y in range(1, h - 1):
                    if random() < 0.5:
                        cave.set(x, y, '.')
            for i in range(0, 10):
                cls.automaton(cave)
            cls.joinall(cave)
            cls.automaton(cave)
            cls.automaton(cave)
            if cls.isok(cave):
                break
        return cave

    @classmethod
    def isok(cls, cave):
        total = 0.0
        space = 0.0
        for y in range(1, cave.height - 1):
            for x in range(1, cave.width - 1):
                total += 1.0
                if cave.isopen(x, y):
                    space += 1.0
        ratio = space / total
        return 0.2 < ratio and ratio < 0.6

    @classmethod
    def automaton(cls, cave):
        for y in range(1, cave.height - 1):
            for x in range(1, cave.width - 1):
                wallcount = 0
                for dy, dx in cls.adjacent:
                    if cave.iswall(x + dx, y + dy):
                        wallcount += 1
                if cave.iswall(x, y):
                    if wallcount < 4:
                        cave.set(x, y, '.')
                else:
                    if wallcount >= 5:
                        cave.set(x, y, '#')

    @classmethod
    def joinall(cls, cave):
        color = 1
        colorof = {}
        groups = {}

        def dig(x, y, color):
            cave.set(x, y, '.')
            colorof[(x, y)] = color

        def join(color):
            color = groups.keys()[0]
            queue = list(groups[color])
            previous = {}
            for xy in queue:
                previous [xy] = xy
            while queue:
                x, y = pt = queue.pop(0)
                if cave.isopen(x, y) and colorof[pt] != color:
                    color2 = colorof[pt]
                    assert color2 in groups
                    while pt != previous.get(pt):
                        dig(pt[0], pt[1], color)
                        dig(pt[0] + 1, pt[1], color)
                        dig(pt[0], pt[1] + 1, color)
                        dig(pt[0] + 1, pt[1] + 1, color)
                        pt = previous.get(pt)
                    combine(color, color2)
                    return
                for dy, dx in cls.randomcardinal():
                    xx, yy = ptt = x + dx, y + dy
                    if ptt not in previous and cave.isvalid(xx, yy):
                        previous[ptt] = pt
                        queue.append(ptt)

        def combine(color1, color2):
            for pt in colorof:
                if colorof[pt] == color2:
                    colorof[pt] = color1
            g1 = groups[color1]
            g2 = groups[color2]
            g1.extend(g2)
            del groups[color2]

        def colorize(x0, y0, color):
            seen = set((x0, y0))
            queue = [(x0, y0)]
            while queue:
                (x, y) = pt = queue.pop()
                colorof[pt] = color
                groups[color].append(pt)
                for dy, dx in cls.randomcardinal():
                    xx, yy = ptt = x + dx, y + dy
                    if ptt not in seen and cave.isopen(xx, yy):
                        seen.add(ptt)
                        queue.append(ptt)

        for y in range(1, cave.height - 1):
            for x in range(1, cave.width - 1):
                if (x, y) not in colorof and cave.isopen(x, y):
                    groups[color] = []
                    colorize(x, y, color)
                    color += 1

        while len(groups) > 1:
            join(1)

    @classmethod
    def generate(cls, p):
        scale = 4 if p.switch.is_pressed else 8
        w = (384 / scale)
        h = (384 / scale)
        cave = cls.init(w, h)
        _, ptiles = tiles.load('16tiles.bmp', 16)
        canvas = cave.render(scale, cls.glyphs, ptiles)
        p.println('enter the cavern!')
        p.printImage(canvas, True)

allgenerators = [Diagnostic, Magic8, Tarot, Potion, Labyrinth, Tiles, Npc, Cave]

class Switch(object):
    def __init__(self, b):
        self.is_pressed = b
class Sim(object):
    def __init__(self):
        self.switch = Switch(True)
        self.ip = network.ip()
        self.generators = list(allgenerators)
        self.i = 1
    def println(self, msg):
        n = len(msg)
        if n < 32:
            pad = (32 - n) * ' '
            print '|' + msg + pad + '|'
        else:
            print '|' + msg[:32] + '|' + msg[32:]
    def printImage(self, img, LaaT):
        path = 'image%d.bmp' % self.i
        img.save(path)
        print '-- saved: %s' % path
        self.i += 1

if __name__ == "__main__":
    args = sys.argv[1:]
    sim = Sim()
    if not args:
        Diagnostic.generate(sim)
    else:
        s = args[0]
        for g in allgenerators:
            if g.name == s:
                g.generate(sim)
                break
        else:
            print 'no generator for %r' % s
