#!/usr/bin/env python3
"""
build_card.py: the status screen (character card).

Reuses the palette, font and dragon sprites from build_title.py, so the
character on the card is the same one from the boot screen, now in costume.

    python build_card.py   ->  assets/card.svg  /  assets/card-static.svg
"""
import os
import math

from build_title import (Layer, rows, blit, paths, text, title, tr, op, HEAD, TAIL_FLAME,
                         VOID, DARK_E, ORB_HI, PURPLE, PURP_SH, CYAN, GREEN, RED, SMOKE,
                         LABEL, OUTLINE, PURP_MD, S, P)

CW, CH = 190, 110          # same pixel size as the title screen, taller canvas
BOX = (12, 17, 72, 73)     # portrait box: x1, y1, x2, y2
PANEL_BG = '#120A1F'

# ---- the dragon, in costume --------------------------------------------------
HEAD_A = list(HEAD)
HEAD_A[6] = '...KLLPPKKNNNPPPPSSK'      # heavy brow
HEAD_A[7] = '...KLPPPKKKKPPPPPSSK'      # flat eyelid: annoyed
HEAD_A[11] = 'KKKKPPPPPPPPPPPPPSSK'     # mouth shut
HEAD_A[12] = 'KBPPPPPPNNPPPPPPPSSK'     # one fang
assert all(len(r) == 20 for r in HEAD_A)

HAT = rows("""
...K...
..KSK..
..KSK..
.KSSSK.
.KSSSK.
.KNNNK.
KSSSSSK
KKKKKKK
""", 'hat')

ROBE = rows("""
.KKKKKKKKKKKKKKKKKK.
KSSSSSSSNNSSSSSSSSSK
KSSSSSSSNNSSSSSSSSSK
KSSSSSSSNNSSSSSSSSSK
""", 'robe')

import build_title as _bt


def blit_dark(L, sprite, x, y):
    """hat and robe: same grid format, dim cyan so they separate from the dragon"""
    old = dict(_bt.SP)
    _bt.SP['S'] = '#0F7F94'
    blit(L, sprite, x, y)
    _bt.SP.clear()
    _bt.SP.update(old)


def frame(L, x1, y1, x2, y2, col, cut=2):
    for x in range(x1 + cut, x2 - cut + 1):
        L.put(x, y1, col); L.put(x, y2, col)
    for y in range(y1 + cut, y2 - cut + 1):
        L.put(x1, y, col); L.put(x2, y, col)
    for i in range(cut):
        L.put(x1 + cut - 1 - i, y1 + i, col); L.put(x2 - cut + 1 + i, y1 + i, col)
        L.put(x1 + cut - 1 - i, y2 - i, col); L.put(x2 - cut + 1 + i, y2 - i, col)


def fill(L, x1, y1, x2, y2, col):
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            L.put(x, y, col)


BASE, FLAME_L, EYE_L, CURSOR = Layer(CW, CH), Layer(CW, CH), Layer(CW, CH), Layer(CW, CH)

# main frame: uneven on purpose. bright border, dim shadow lines on the bottom + right
frame(BASE, 6, 6, 183, 104, PURPLE, cut=3)
for x in range(10, 180):
    BASE.put(x, 102, PURP_SH)
for y in range(10, 101):
    BASE.put(181, y, PURP_SH)

# tab
fill(BASE, 12, 2, 54, 12, DARK_E)
frame(BASE, 12, 2, 54, 12, PURPLE, cut=1)
text(BASE, 'STATUS', 17, 4, 1, 1, CYAN)

# portrait box
x1, y1, x2, y2 = BOX
fill(BASE, x1, y1, x2, y2, PANEL_BG)
OXc, OYc, ORc = 44, 40, 22
for y in range(y1 + 1, y2):
    for x in range(x1 + 1, x2):
        d = math.hypot(x + .5 - OXc, y + .5 - OYc)
        chk = (x + y) % 2 == 0
        if d < ORc * .6:
            BASE.put(x, y, ORB_HI)
        elif d < ORc * .78:
            BASE.put(x, y, ORB_HI if chk else DARK_E)
        elif d < ORc - 1:
            BASE.put(x, y, DARK_E)
        elif d < ORc + .5 and chk:
            BASE.put(x, y, PURP_SH)
for sx, sy, sc in [(15, 21, '#3A2A5C'), (67, 22, SMOKE), (16, 62, '#157F8F'),
                   (66, 58, '#6B2FA8'), (60, 20, '#157F8F'), (22, 30, '#3A2A5C')]:
    BASE.put(sx, sy, sc)
for y in range(68, y2):                              # floor
    for x in range(x1 + 1, x2):
        BASE.put(x, y, '#241240' if (x + y) % 2 == 0 else DARK_E)
for x in range(x1 + 1, x2):
    BASE.put(x, 68, PURP_SH)
frame(BASE, x1, y1, x2, y2, PURPLE, cut=2)

# the mage: robe, head, hat (back to front)
hx0, hy0 = 26, 28
blit_dark(BASE, ROBE, hx0, hy0 + 16 * S)
blit(BASE, HEAD_A, hx0, hy0)
blit_dark(BASE, HAT, hx0 + 8 * S, hy0 - 5 * S)
blit(FLAME_L, TAIL_FLAME, 13, 40)
for x in range(hx0 + 8 * S, hx0 + 12 * S):          # eyelid for the blink
    for y in range(hy0 + 7 * S, hy0 + 11 * S):
        EYE_L.put(x, y, PURP_MD)
    for y in range(hy0 + 9 * S, hy0 + 10 * S):
        EYE_L.put(x, y, OUTLINE)
STEAM = [(hx0 + 2, hy0 + 18, 2.2, 0.0), (hx0 + 4, hy0 + 18, 2.6, 1.1)]

# name, class, rage meter
text(BASE, 'AIN SHAMSUDHEEN', 78, 18, 1, 1, SMOKE)
_unused = Layer(CW, CH)
title(BASE, _unused, 'ANGRY', 78, 28, s=2, gap=2, bevel=False, shadow=1)
title(BASE, _unused, 'FIRE MAGE', 78, 45, s=2, gap=2, bevel=False, shadow=1)
text(BASE, 'RAGE', 78, 64, 1, 1, SMOKE)
for i in range(6):
    fill(BASE, 104 + i * 5, 65, 107 + i * 5, 69, RED)
text(BASE, 'MAX', 137, 64, 1, 1, LABEL)

# divider + intro
for x in range(12, 178):
    BASE.put(x, 78, PURP_SH if x % 2 else DARK_E)
text(BASE, 'I WORK BELOW THE APP LAYER.', 12, 84, 1, 1, SMOKE)
end = text(BASE, [('BUGS GET ', SMOKE), ('BURNED.', GREEN)], 12, 93, 1, 1)
fill(CURSOR, end + 3, 93, end + 6, 99, GREEN)


def build(animate):
    an = (lambda s: s) if animate else (lambda s: '')
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CW} {CH}" width="{CW * P}" '
         f'height="{CH * P}" shape-rendering="crispEdges" role="img" '
         f'aria-label="Status screen. Ain Shamsudheen, class: angry fire mage. A grumpy purple dragon in a wizard hat. Rage: max.">',
         '<title>Status: Ain Shamsudheen, angry fire mage</title>',
         f'<rect width="{CW}" height="{CH}" fill="{VOID}"/>', paths(BASE)]
    if animate:
        o.append(f'<g opacity="0">{paths(EYE_L)}{op("0;1;0", "0;0.93;0.97", 5.0)}</g>')
    o.append(f'<g>{paths(FLAME_L)}{an(tr("0 0;0 -2", "0;0.5", 0.7))}</g>')
    for sx, sy, dur, begin in STEAM:
        o.append(f'<rect x="{sx}" y="{sy}" width="2" height="2" fill="{SMOKE}" opacity="0.0">'
                 f'{an(tr("0 0;0 -2;2 -4;0 -6", "0;0.25;0.5;0.75", dur, begin=begin))}'
                 f'{an(op("0.9;0.9;0.5;0.2", "0;0.25;0.5;0.75", dur, begin))}</rect>')
    o.append(f'<g>{paths(CURSOR)}{an(op("1;0", "0;0.5", 1.0))}</g>')
    o.append('</svg>')
    return ''.join(o)


if __name__ == '__main__':
    os.makedirs('assets', exist_ok=True)
    for name, flag in [('card.svg', True), ('card-static.svg', False)]:
        with open(os.path.join('assets', name), 'w') as f:
            f.write(build(flag))
        print('wrote', name, f'({os.path.getsize(os.path.join("assets", name)) // 1024} KB)')
