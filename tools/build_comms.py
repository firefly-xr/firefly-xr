#!/usr/bin/env python3
"""
build_comms.py: Connect With Me / Communications screen.
Reuses the palette, font, and frame styling from build_title.py and build_card.py.
Includes custom pixel-art logos for LinkedIn, Email, HackerRank, and CodePen.

    python build_comms.py -> assets/comms.svg / assets/comms-static.svg
"""
import os
import math
from build_title import (Layer, paths, text, tr, op,
                         VOID, DARK_E, ORB_HI, PURPLE, PURP_SH, PURP_MD, PURP_HI,
                         CYAN, GREEN, GREEN_DK, GREEN_PALE, RED, SMOKE, SMOKE_DK,
                         OUTLINE, LABEL, TRACE, P)

CW, CH = 190, 105
PANEL_BG = '#120A1F'


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


def draw_logo(L, x, y, sprite, fg, bg, icon_col='#FFFFFF'):
    for j, row in enumerate(sprite):
        for i, ch in enumerate(row):
            if ch == '#':
                L.put(x + i, y + j, fg)
            elif ch == '.':
                L.put(x + i, y + j, bg)
            elif ch == 'W':
                L.put(x + i, y + j, icon_col)


BASE, WAVE_L, CURSOR_L = Layer(CW, CH), Layer(CW, CH), Layer(CW, CH)

# Main frame
frame(BASE, 6, 6, 183, 99, PURPLE, cut=3)
for x in range(10, 180):
    BASE.put(x, 97, PURP_SH)
for y in range(10, 96):
    BASE.put(181, y, PURP_SH)

# Tab
fill(BASE, 12, 2, 54, 12, DARK_E)
frame(BASE, 12, 2, 54, 12, PURPLE, cut=1)
text(BASE, 'COMMS', 17, 4, 1, 1, CYAN)

# Left Side: Satellite / Antenna Dish Box
ax1, ay1, ax2, ay2 = 12, 17, 50, 92
fill(BASE, ax1, ay1, ax2, ay2, PANEL_BG)
frame(BASE, ax1, ay1, ax2, ay2, PURPLE, cut=2)

# Antenna Tower / Dish base
for y in range(65, 80):
    w = (y - 65) // 3
    for x in range(31 - w, 32 + w):
        BASE.put(x, y, PURP_SH)
    BASE.put(31, y, SMOKE_DK)

# Dish arc
dish_cx, dish_cy = 31, 55
for dx in range(-11, 12):
    dy = int((dx * dx) * 0.08)
    BASE.put(dish_cx + dx, dish_cy - dy, PURP_HI)
    BASE.put(dish_cx + dx, dish_cy - dy + 1, PURPLE)

# Feed horn
for y in range(dish_cy - 7, dish_cy - 1):
    BASE.put(dish_cx, y, SMOKE)
BASE.put(dish_cx - 1, dish_cy - 7, GREEN)
BASE.put(dish_cx + 1, dish_cy - 7, GREEN)

# Sub labels under antenna
text(BASE, 'ONLINE', 18, 83, 1, 1, GREEN)

# Animated signal waves radiating upward
for r in [9, 14, 19]:
    for angle in range(-45, 46, 5):
        rad = math.radians(angle)
        wx = int(dish_cx + r * math.sin(rad))
        wy = int((dish_cy - 7) - r * math.cos(rad))
        if ax1 + 2 <= wx <= ax2 - 2 and ay1 + 2 <= wy <= ay2 - 2:
            WAVE_L.put(wx, wy, CYAN)

# 7x7 pixel logos
LOGO_LI = [
    "#######",
    "#.....#",
    "#.W.W.#",
    "#...W.#",
    "#.W.W.#",
    "#.....#",
    "#######",
]

LOGO_MAIL = [
    "#######",
    "#W...W#",
    "#.W.W.#",
    "#..W..#",
    "#.....#",
    "#.....#",
    "#######",
]

LOGO_HR = [
    "#######",
    "#.W.W.#",
    "#.W.W.#",
    "#.WWW.#",
    "#.W.W.#",
    "#.W.W.#",
    "#######",
]

LOGO_CP = [
    "#######",
    "#..W..#",
    "#.W.W.#",
    "#WW.WW#",
    "#.W.W.#",
    "#..W..#",
    "#######",
]

# Right Side: Channels with Logos
channels = [
    (LOGO_LI, CYAN, '#0B3045', 'LINKEDIN', 'AIN SHAMSUDHEEN', CYAN, 18),
    (LOGO_MAIL, RED, '#3A1215', 'EMAIL', 'AINSHAMSUDHEEN123', RED, 34),
    (LOGO_HR, GREEN, '#0C3B1C', 'HACKERRANK', 'AINSHAMSUDHEEN11', GREEN, 50),
    (LOGO_CP, PURP_HI, '#2D1452', 'CODEPEN', 'AIN-SHAMSUDHEEN', PURP_HI, 66),
]

for sprite, fg, bg, label_txt, val_txt, col, y in channels:
    # Draw pixel brand logo
    draw_logo(BASE, 56, y + 2, sprite, fg, bg)
    # Channel name and handle
    text(BASE, label_txt, 67, y, 1, 1, col)
    text(BASE, val_txt, 67, y + 8, 1, 1, SMOKE)

# Transmission status line
end = text(BASE, 'SIGNAL LOCKED // TRANSMIT', 56, 83, 1, 1, LABEL)
fill(CURSOR_L, end + 3, 83, end + 6, 89, GREEN)


def build(animate):
    an = (lambda s: s) if animate else (lambda s: '')
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CW} {CH}" width="{CW * P}" '
         f'height="{CH * P}" shape-rendering="crispEdges" role="img" '
         f'aria-label="Connect Channels screen for Ain Shamsudheen: LinkedIn, Email, HackerRank, CodePen with brand logos.">',
         '<title>Comms: Connect With Me</title>',
         f'<rect width="{CW}" height="{CH}" fill="{VOID}"/>', paths(BASE)]

    if animate:
        # Radiating radio signal wave pulse
        o.append(f'<g>{paths(WAVE_L)}{an(op("0.2;1;0.2", "0;0.5;1", 1.6))}</g>')
        # Blinking cursor
        o.append(f'<g>{paths(CURSOR_L)}{an(op("1;0", "0;0.5", 0.9))}</g>')
        # Power LED
        o.append(f'<rect x="180" y="8" width="2" height="2" fill="{GREEN}">'
                 f'{an(op("1;0.4", "0;0.5", 2.0))}</rect>')
    else:
        o.append(paths(WAVE_L))
        o.append(paths(CURSOR_L))
        o.append(f'<rect x="180" y="8" width="2" height="2" fill="{GREEN}"/>')

    o.append('</svg>')
    return ''.join(o)


if __name__ == '__main__':
    os.makedirs('assets', exist_ok=True)
    for name, flag in [('comms.svg', True), ('comms-static.svg', False)]:
        with open(os.path.join('assets', name), 'w') as f:
            f.write(build(flag))
        print('wrote', name, f'({os.path.getsize(os.path.join("assets", name)) // 1024} KB)')
