#!/usr/bin/python
#
# notes:
#  - 32 columns of text at normal font

from Adafruit_Thermal import *
from PIL import Image
from gpiozero import LED, Button
from signal import pause
from socket import socket, AF_INET, SOCK_DGRAM
from subprocess import call
from random import choice, random, randint, shuffle
import re

vowels = set('aeiouy')

def a_an(noun):
    if noun and noun[0] in vowels:
        return 'an'
    else:
        return 'a'

class Generator(object):
    @classmethod
    def generate(cls, p):
        p.println('unimplemented %r' % cls)

class Diagnostic(Generator):

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

class Map(object):
    def __init__(self, width, height, fill='#'):
        self.width = width
        self.height = height
        self.grid = [[fill for i in range(width)] for j in range(height)]

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

class Labyrinth(Generator):
    glyphs = {
        '#': 0,
        '.': 13,
    }

    @classmethod
    def init(cls, w, h):
        maze = Map(w, h, '#')
        for x in range(1, w - 1, 2):
            for y in range(1, h - 1, 2):
                maze.set(x, y, '.')
        return maze

    @classmethod
    def backtrackx(cls, w, h):
        return cls.backtrack(w, h, ds=[(2, 0), (2, 0), (0, 2), (-2, 0), (-2, 0), (0, -2)])

    @classmethod
    def backtracky(cls, w, h):
        return cls.backtrack(w, h, ds=[(2, 0), (0, 2), (0, 2), (-2, 0), (0, -2), (0, -2)])

    @classmethod
    def backtrack(cls, w, h, ds=[(2, 0), (0, 2), (-2, 0), (0, -2)]):
        maze = cls.init(w, h)
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
    def kruskal(cls, w, h):
        maze = Map(w, h, '#')
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

    @classmethod
    def generate(cls, p):
        scale = 8 if p.switch.is_pressed else 16
        w = (384 / scale) - 1
        h = (384 / scale) - 1
        f = choice([cls.kruskal, cls.backtrack, cls.backtrackx, cls.backtracky])
        maze = f(w, h)
        canvas = maze.render(scale, cls.glyphs, p.tiles)
        p.println('enter the labyrinth!')
        p.printImage(canvas, True)

class Tiles(Generator):

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
    glyphs = {
        '#': 0,
        '.': 13,
    }

    adjacent = [
        (-1, -1), (-1, +0), (-1, +1),
        (+0, -1),           (+0, +1),
        (+1, -1), (+1, +0), (+1, +1)
    ]

    @classmethod
    def init(cls, w, h):
        attempts = 10
        for i in range(0, attempts):
            cave = Map(w, h, '#')
            for x in range(1, w - 1):
                for y in range(1, h - 1):
                    if random() < 0.5:
                        cave.set(x, y, '.')
            for i in range(0, 10):
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
                if cave.get(x, y) == '.':
                    space += 1.0
        ratio = space / total
        return 0.2 < ratio and ratio < 0.6

    @classmethod
    def automaton(cls, cave):
        for y in range(1, cave.height - 1):
            for x in range(1, cave.width - 1):
                wallcount = 0
                for dy, dx in cls.adjacent:
                    if cave.get(x + dx, y + dy) == '#':
                        wallcount += 1
                if cave.get(x, y) == '#':
                    if wallcount < 4:
                        cave.set(x, y, '.')
                else:
                    if wallcount >= 5:
                        cave.set(x, y, '#')

    @classmethod
    def generate(cls, p):
        scale = 4 if p.switch.is_pressed else 8
        w = (384 / scale)
        h = (384 / scale)
        cave = cls.init(w, h)
        canvas = cave.render(scale, cls.glyphs, p.tiles)
        p.println('enter the cavern!')
        p.printImage(canvas, True)
