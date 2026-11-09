#!/usr/bin/env python3
"""
build_title.py: boot screen for the profile README.

Every pixel in the output is a rect inside a path. No image editor, no exports.
Sprites are character grids, the font is a 5x7 table, colours are a dict.
Change a letter in a grid, rerun, the art changes.

    python build_title.py   ->  assets/title.svg         (animated)
                                assets/title-static.svg  (no motion)
"""
import math
import os
import random

W, H, P = 190, 70, 5          # canvas in art-pixels, screen px per art-pixel
S = 2                         # dragon sprite scale
GROUND = 56                   # y of the floor line

# ---- palette: every colour has a job ----------------------------------------
VOID       = '#0B0612'        # background. never pure black
VOID_DEEP  = '#05020A'        # screen-edge dither
DARK_E     = '#1A0F2E'        # dark energy: floor, orb body
ORB_HI     = '#2A1050'
PURPLE     = '#B026FF'        # neon purple: the title, the floor line
PURP_SH    = '#5B1A99'        # dragon shadow
PURP_MD    = '#9B2FE8'        # dragon base
PURP_HI    = '#C77DFF'        # dragon light
CYAN       = '#22E4FF'
TRACE      = '#124A57'        # dim cyan for the pcb traces in the floor
GREEN      = '#39FF6A'
GREEN_DK   = '#17A34A'
GREEN_PALE = '#C9FFD8'
RED        = '#FF2A4D'        # terror red: tongue + power LED. that is all
RED_DK     = '#5A0F2B'
SMOKE      = '#D9D6E0'
SMOKE_DK   = '#A9A3B8'
OUTLINE    = '#2E1058'
LABEL      = '#7A5BA8'

SP = {  # sprite key -> colour
    'K': OUTLINE, 'S': PURP_SH, 'P': PURP_MD, 'L': PURP_HI,
    'B': SMOKE, 'b': SMOKE_DK, 'W': '#F4F2F8', 'C': CYAN,
    'N': GREEN, 'n': GREEN_DK, 'Y': GREEN_PALE,
    'm': RED_DK, 'R': RED,
}


# ---- plumbing ---------------------------------------------------------------
class Layer:
    def __init__(self, w=None, h=None):
        self.px = {}
        self.w, self.h = w or W, h or H

    def put(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[(x, y)] = c


def rows(s, name):
    r = s.strip().split('\n')
    assert len({len(x) for x in r}) == 1, f'{name}: ragged rows {[len(x) for x in r]}'
    return r


def blit(L, sprite, x, y, s=None):
    s = s or S
    for j, row in enumerate(sprite):
        for i, ch in enumerate(row):
            if ch != '.':
                for dy in range(s):
                    for dx in range(s):
                        L.put(x + i * s + dx, y + j * s + dy, SP[ch])


def paths(L):
    """one <path> per colour, horizontal runs merged"""
    by = {}
    for (x, y), c in L.px.items():
        by.setdefault(c, {}).setdefault(y, []).append(x)
    out = []
    for c, ys in by.items():
        d = []
        for y, xs in sorted(ys.items()):
            xs.sort()
            s = p = xs[0]
            for x in xs[1:] + [None]:
                if x is not None and x == p + 1:
                    p = x
                    continue
                d.append(f'M{s} {y}h{p - s + 1}v1h-{p - s + 1}z')
                if x is not None:
                    s = p = x
        out.append(f'<path fill="{c}" d="{"".join(d)}"/>')
    return ''.join(out)


# ---- font: 5x7, drawn by hand, because svg-as-image cannot load fonts -------
FONT_SRC = {
    'A': '.###./#...#/#...#/#####/#...#/#...#/#...#',
    'B': '####./#...#/#...#/####./#...#/#...#/####.',
    'C': '.###./#...#/#..../#..../#..../#...#/.###.',
    'F': '#####/#..../#..../####./#..../#..../#....',
    'G': '.###./#...#/#..../#.###/#...#/#...#/.###.',
    'K': '#...#/#..#./#.#../##.../#.#../#..#./#...#',
    'W': '#...#/#...#/#...#/#.#.#/#.#.#/##.##/#...#',
    'D': '####./#...#/#...#/#...#/#...#/#...#/####.',
    'E': '#####/#..../#..../####./#..../#..../#####',
    'H': '#...#/#...#/#...#/#####/#...#/#...#/#...#',
    'I': '.###./..#../..#../..#../..#../..#../.###.',
    'L': '#..../#..../#..../#..../#..../#..../#####',
    'M': '#...#/##.##/#.#.#/#.#.#/#...#/#...#/#...#',
    'N': '#...#/##..#/#.#.#/#..##/#...#/#...#/#...#',
    'O': '.###./#...#/#...#/#...#/#...#/#...#/.###.',
    'P': '####./#...#/#...#/####./#..../#..../#....',
    'R': '####./#...#/#...#/####./#.#../#..#./#...#',
    'S': '.####/#..../#..../.###./....#/....#/####.',
    'T': '#####/..#../..#../..#../..#../..#../..#..',
    'U': '#...#/#...#/#...#/#...#/#...#/#...#/.###.',
    'X': '#...#/#...#/.#.#./..#../.#.#./#...#/#...#',
    'Y': '#...#/#...#/.#.#./..#../..#../..#../..#..',
    '0': '.###./#...#/#..##/#.#.#/##..#/#...#/.###.',
    '1': '..#../.##../..#../..#../..#../..#../.###.',
    '2': '.###./#...#/....#/.###./#..../#..../#####',
    '3': '####./....#/....#/.###./....#/....#/####.',
    '4': '#...#/#...#/#...#/#####/....#/....#/....#',
    '5': '#####/#..../#..../####./....#/....#/####.',
    '6': '.###./#..../#..../####./#...#/#...#/.###.',
    '7': '#####/....#/....#/...#./..#../.#.../#....',
    '8': '.###./#...#/#...#/.###./#...#/#...#/.###.',
    '9': '.###./#...#/#...#/.####/....#/....#/.###.',
    'J': '....#/....#/....#/....#/#...#/#...#/.###.',
    'Q': '.###./#...#/#...#/#...#/#.#.#/#..#./.##.#',
    'V': '#...#/#...#/#...#/#...#/.#.#./.#.#./..#..',
    'Z': '#####/....#/...#./..#../.#.../#..../#####',
    ':': '...../..##./..##./...../..##./..##./.....',
    '-': '...../...../...../#####/...../...../.....',
    '+': '...../..#../..#../#####/..#../..#../.....',
    '&': '.##../#..#./.#.#./..#../.#.#./#..#./.##.#',
    ',': '...../...../...../...../...../..##./.##..',
    '@': '.###./#...#/...##/#.#.#/#.#.#/#...#/.###.',
    '[': '.###./.#.../.#.../.#.../.#.../.#.../.###.',
    ']': '.###./...#./...#./...#./...#./...#./.###.',
    '(': '..##./.#.../.#.../.#.../.#.../.#.../..##.',
    ')': '.##../...#./...#./...#./...#./...#./.##..',
    '!': '..#../..#../..#../..#../..#../...../..#..',
    '?': '.###./#...#/....#/..##./..#../...../..#..',
    '.': '...../...../...../...../...../.##../.##..',
    '/': '....#/....#/...#./..#../.#.../#..../#....',
    '>': '#..../.#.../..#../...#./..#../.#.../#....',
    ' ': '...../...../...../...../...../...../.....',
}
FONT = {k: v.split('/') for k, v in FONT_SRC.items()}
for _k, _g in FONT.items():
    assert len(_g) == 7 and all(len(r) == 5 for r in _g), f'glyph {_k!r} is malformed'


def glyph_px(ch, x, y, s=1):
    for j, row in enumerate(FONT[ch]):
        for i, c in enumerate(row):
            if c == '#':
                for dy in range(s):
                    for dx in range(s):
                        yield (x + i * s + dx, y + j * s + dy)


def text(L, segs, x, y, s=1, gap=1, color=None):
    if isinstance(segs, str):
        segs = [(segs, color)]
    for chunk, col in segs:
        for ch in chunk:
            for p in glyph_px(ch, x, y, s):
                L.put(*p, col)
            x += 5 * s + gap
    return x - gap


def title(L, G, word, x, y, s=3, gap=3, bevel=True, shadow=None):
    """big logo: lit top edge, shaded bottom edge, hard drop shadow.
    G gets a cyan slice that flashes now and then (a one-row glitch).
    bevel=False gives a flat fill, which reads better at small sizes."""
    sh = s if shadow is None else shadow
    pts = set()
    cx = x
    for ch in word:
        pts |= set(glyph_px(ch, cx, y, s))
        cx += (2 * s + gap) if ch == ' ' else (5 * s + gap)
    for a, b in pts:
        if (a + sh, b + sh) not in pts:
            L.put(a + sh, b + sh, '#1D0A33')
    for a, b in pts:
        if y + 3 * s <= b < y + 4 * s and (a - s, b) not in pts:
            G.put(a - s, b, CYAN)
    for a, b in pts:
        if bevel and (a, b - 1) not in pts:
            c = '#D58BFF'
        elif bevel and (a, b + 1) not in pts:
            c = '#7A1FC4'
        else:
            c = PURPLE
        L.put(a, b, c)


# ---- sprites: the dragon, facing left ----------------------------------------
HEAD = rows("""
.......K.......K....
......KBK.....KBK...
......KbK.....KbK...
......KKKKKKKKKKK...
.....KLLLPPPPPPSSK..
....KLLLPPPNPPPPSSK.
...KLLPPPPNNNPPPPSSK
...KLPPPPKKPPPPPPSSK
...KLPPPKCWKPPPPPSSK
.KKKPPPPKCCKPPPPPSSK
KSPPPPPPPKKPPPPPPSSK
mmmmPPPPPPPPPPPPPSSK
mRmmPPPPNNPPPPPPPSSK
KLPPPPPPPPPPPPPPPSSK
.KKKKPPSSSSSSSSSSSK.
.....KKKKKKKKKKKKK..
""", 'head')

BODY = rows("""
..KKKKKKKKKKK....
.KPPPPPPPPPPSK...
KPBBBPPPPPNPSSKN.
KbbbbPPPPPPPPSSK.
KBBBBPPPNPPPPSSKN
KbbbbPPPPPPPNSSK.
KBBBBPPPPNPPPSSKN
KbbbbPPPPPPPPSSK.
.KBBBPPPPPPPSSK..
..KKSSSSSSSSKK...
...KKKKKKKKKK....
""", 'body')

WING = rows("""
..........KK..
.........KPPK.
........KPSSSK
.......KPSSSSK
......KPSSNSSK
.....KPSSSSSSK
....KPSSKSSKSK
...KPSSSKSKSKK
...KKSSSKKSKK.
....KKSKK.KK..
.....KK.......
""", 'wing')

TAIL = rows("""
........KKK...
.......KPPPK..
.......KPPSK..
......KPPSK...
......KPPSK...
.....KPPSK....
KKKKKPPSK.....
PPNPPNPSK.....
PSSSSSSK......
KKKKKKK.......
""", 'tail')

FOOT = rows("""
.KPPK.
KPPPPK
KBKBKK
""", 'foot')

ARM = rows("""
.KK.
KPPK
.KK.
""", 'arm')

TAIL_FLAME = rows("""
..n..
.nNn.
.NYN.
nNYNn
nNYNn
.nNn.
..n..
""", 'tail flame')

MOUTH_FLAME = rows("""
..n.n...........
.nNnNn..........
nNNNNNnn........
nNNYYNNNnn......
nNYYYYNNNNnnn...
NNYYYYYYYYNNNNnn
nNYYYYNNNNnnn...
nNNYYNNNnn......
nNNNNNnn........
.nNnNn..........
..n.n...........
""", 'mouth flame')


# ---- scene ------------------------------------------------------------------
hx, hy = 110, GROUND - 25 * S           # dragon origin (snout, horn tips)
OX, OY, OR = hx + 46, hy + 16, 20       # dark-energy orb behind the dragon
BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]

BASE, GLITCH = Layer(), Layer()
PRESS, CURSOR = Layer(), Layer()
WING_L, BODY_L, HEAD_L = Layer(), Layer(), Layer()
MOUTH_L, TAILF_L, EYE_L = Layer(), Layer(), Layer()

# dragon, back to front. one sprite pixel = S x S art pixels
blit(WING_L, WING, hx + 16 * S, hy + 4 * S)
blit(BODY_L, BODY, hx + 8 * S, hy + 13 * S)
blit(BODY_L, TAIL, hx + 23 * S, hy + 14 * S)
blit(BODY_L, FOOT, hx + 9 * S, hy + 22 * S)
blit(BODY_L, FOOT, hx + 16 * S, hy + 22 * S)
blit(BODY_L, ARM, hx + 6 * S, hy + 18 * S)
blit(HEAD_L, HEAD, hx, hy)
blit(MOUTH_L, MOUTH_FLAME, hx - 16 * S, hy + 6 * S)
blit(TAILF_L, TAIL_FLAME, hx + 30 * S, hy + 9 * S)
for x in range(hx + 8 * S, hx + 12 * S):              # eyelid for the blink
    for y in range(hy + 7 * S, hy + 11 * S):
        EYE_L.put(x, y, PURP_MD)
    for y in range(hy + 9 * S, hy + 10 * S):
        EYE_L.put(x, y, OUTLINE)

# stars keep clear of the text column, the dragon and the orb
STAR_COLS = ['#3A2A5C', '#157F8F', SMOKE, '#6B2FA8']
OCC = set()
for _l in (WING_L, BODY_L, HEAD_L, MOUTH_L, TAILF_L):
    OCC |= set(_l.px)


def blocked(x, y):
    if x < 94 and y < GROUND:
        return True
    if any((x + dx, y + dy) in OCC for dx in range(-2, 3) for dy in range(-2, 3)):
        return True
    return math.hypot(x + .5 - OX, y + .5 - OY) < OR + 2


def scatter_stars():
    rng = random.Random(1103)
    out = []
    while len(out) < 34:
        x, y = rng.randrange(1, W - 1), rng.randrange(1, GROUND - 2)
        if blocked(x, y) or any(abs(x - a) < 3 and abs(y - b) < 3 for a, b, _ in out):
            continue
        out.append((x, y, rng.choices(STAR_COLS, [5, 3, 1, 2])[0]))
    return out


STARS = scatter_stars()
TWINKLE, STILL = STARS[:5], STARS[5:]
for sx, sy, sc in STILL:
    BASE.put(sx, sy, sc)

# hand-placed sparkles (plus shapes)
for cx_, cy_, col in [(84, 9, CYAN), (100, 6, SMOKE), (96, 49, PURPLE)]:
    for dx, dy in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
        BASE.put(cx_ + dx, cy_ + dy, col)

# orb: dither between two tones, no gradients
for y in range(OY - OR - 1, OY + OR + 2):
    for x in range(OX - OR - 1, OX + OR + 2):
        d = math.hypot(x + .5 - OX, y + .5 - OY)
        chk = (x + y) % 2 == 0
        if d < OR * .6:
            c = ORB_HI
        elif d < OR * .75:
            c = ORB_HI if chk else DARK_E
        elif d < OR - 1:
            c = DARK_E
        elif d < OR + .5:
            c = PURP_SH if chk else DARK_E
        else:
            continue
        BASE.put(x, y, c)

# floor: dithered neon line, dark-energy strip, pcb traces
for x in range(W):
    BASE.put(x, GROUND, PURPLE if x % 2 == 0 else PURP_SH)
for y in range(GROUND + 1, H):
    for x in range(W):
        BASE.put(x, y, '#241240' if (y == GROUND + 1 and x % 2) else DARK_E)


def trace(x1, y1, x2, y2):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            BASE.put(x, y, TRACE)


trace(3, 58, 18, 58); trace(18, 58, 18, 60); trace(18, 60, 34, 60)
trace(48, 59, 70, 59); trace(70, 59, 70, 60); trace(70, 60, 84, 60)
trace(96, 58, 110, 58); trace(110, 58, 110, 60); trace(110, 60, 122, 60)
trace(138, 59, 166, 59); trace(166, 59, 166, 58); trace(166, 58, 180, 58)
for v in [(34, 60), (84, 60), (122, 60), (138, 59), (180, 58), (3, 58)]:
    BASE.put(*v, CYAN)

# screen-edge dither
for y in range(H):
    for x in range(W):
        d = min(x, W - 1 - x, y, H - 1 - y)
        if d < 5 and BAYER[y % 4][x % 4] / 16 < (5 - d) / 5 * .9:
            BASE.put(x, y, VOID_DEEP)

# text
text(BASE, 'ROM 1.0', 6, 4, 1, 1, LABEL)
title(BASE, GLITCH, 'AIN', 6, 13)
text(BASE, 'SHAMSUDHEEN', 6, 37, 1, 1, SMOKE)
text(BASE, '>', 6, 47, 1, 1, GREEN)
text(PRESS, 'PRESS START', 14, 47, 1, 1, GREEN)
for x in range(72, 76):
    for y in range(37, 44):
        CURSOR.put(x, y, GREEN)
text(BASE, [('SYSTEMS', CYAN), (' / ', PURPLE), ('EMBEDDED', CYAN),
            (' / ', PURPLE), ('LINUX', CYAN)], 6, 62)

EMBERS = [(88, 15, GREEN, 2.6, 0.0), (96, 14, GREEN_PALE, 3.1, 0.9),
          (84, 17, GREEN, 2.9, 1.7), (173, 21, GREEN, 2.4, 0.4),
          (177, 21, GREEN_PALE, 3.3, 1.5)]


# ---- assemble ---------------------------------------------------------------
def tr(values, times, dur, mode='discrete', begin=0):
    kt = f' keyTimes="{times}"' if times else ''
    return (f'<animateTransform attributeName="transform" type="translate" values="{values}"{kt} '
            f'dur="{dur}s" calcMode="{mode}" begin="{begin}s" repeatCount="indefinite"/>')


def op(values, times, dur, begin=0):
    return (f'<animate attributeName="opacity" values="{values}" keyTimes="{times}" '
            f'dur="{dur}s" calcMode="discrete" begin="{begin}s" repeatCount="indefinite"/>')


def build(animate):
    an = (lambda s: s) if animate else (lambda s: '')
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W * P}" '
         f'height="{H * P}" shape-rendering="crispEdges" role="img" '
         f'aria-label="Ain Shamsudheen. Systems, embedded, Linux. A purple pixel dragon breathing green fire.">',
         '<title>Ain Shamsudheen: systems, embedded, linux</title>',
         f'<rect width="{W}" height="{H}" fill="{VOID}"/>', paths(BASE)]

    for i, (sx, sy, sc) in enumerate(TWINKLE):
        o.append(f'<rect x="{sx}" y="{sy}" width="1" height="1" fill="{sc}">'
                 f'{an(op("1;0.15", "0;0.5", 1.6 + i * .7, i * .4))}</rect>')

    o.append(f'<g>{paths(WING_L)}{an(tr("0 0;0 -2", "0;0.5", 1.4))}</g>')
    o.append(paths(BODY_L))
    o.append(f'<g>{paths(TAILF_L)}{an(tr("0 0;0 -2", "0;0.5", 0.5))}</g>')

    head = paths(HEAD_L)
    if animate:
        head += f'<g opacity="0">{paths(EYE_L)}{op("0;1;0", "0;0.93;0.97", 4.2)}</g>'
    head += f'<g>{paths(MOUTH_L)}{an(tr("0 0;-2 0;-4 0;-2 0", "0;0.25;0.5;0.75", 0.6))}</g>'
    o.append(f'<g>{head}{an(tr("0 0;0 2", "0;0.5", 1.4))}</g>')

    for ex, ey, ec, dur, begin in EMBERS:
        o.append(f'<rect x="{ex}" y="{ey}" width="1" height="1" fill="{ec}">'
                 f'{an(tr("0 0;-2 -3;0 -6;-2 -9;0 -12", "0;0.2;0.4;0.6;0.8", dur, begin=begin))}'
                 f'{an(op("1;1;1;0.6;0.25", "0;0.2;0.4;0.6;0.8", dur, begin))}</rect>')

    o.append(f'<g>{paths(PRESS)}{an(op("1;0", "0;0.6", 1.4))}</g>')
    o.append(f'<g>{paths(CURSOR)}{an(op("1;0", "0;0.5", 1.0))}</g>')
    if animate:
        o.append(f'<g opacity="0">{paths(GLITCH)}{op("0;1;0;1;0", "0;0.90;0.92;0.94;0.96", 6)}</g>')

    # power LED, like the one on the left of a GBA screen
    o.append(f'<rect x="1" y="34" width="1" height="1" fill="{RED}">'
             f'{an(op("1;0.5", "0;0.5", 2.4))}</rect>')
    if animate:
        o.append(f'<rect width="{W}" height="2" fill="#fff" opacity="0.04">'
                 f'{tr(f"0 -2;0 {H}", None, 9, "linear")}</rect>')
    o.append('</svg>')
    return ''.join(o)


if __name__ == '__main__':
    os.makedirs('assets', exist_ok=True)
    for name, flag in [('title.svg', True), ('title-static.svg', False)]:
        with open(os.path.join('assets', name), 'w') as f:
            f.write(build(flag))
        print('wrote', name, f'({os.path.getsize(os.path.join("assets", name)) // 1024} KB)')
