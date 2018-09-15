from os.path import dirname, realpath
from random import choice, random, shuffle

base = dirname(realpath(__file__))

def load(name):
    f = open(base + '/' + name)
    names = []
    for line in f:
        names.append(line.strip())
    return names

namedata = {
    'F': load('names-F.txt'),
    'M': load('names-M.txt'),
    'S': load('names-S.txt'),
}

traitdata = load('traits.txt')

namedata['N'] = []
namedata['N'].extend(namedata['F'])
namedata['N'].extend(namedata['M'])

def given(mfn):
    return choice(namedata[mfn])

def sur():
    return choice(namedata['S'])

def createname(mfn):
    n = random()
    if n < 0.1:
        parts = [given(mfn), given(mfn), sur()]
    elif n < 0.2:
        parts = [given(mfn), sur(), sur()]
    elif n < 0.4:
        parts = [given(mfn)]
    else:
        parts = [given(mfn), sur()]
    return ' '.join(parts)

def choosetraits(n):
    shuffle(traitdata)
    return traitdata[:n]
