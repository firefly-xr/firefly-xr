#!/usr/bin/env python3
"""
build_quests.py: Currently Working On / Quest Log screen.
Reuses the palette, font, and frame styling from build_title.py and build_card.py.

    python build_quests.py -> assets/quests.svg / assets/quests-static.svg
"""
import os
import math
from build_title import (Layer, paths, text, tr, op,
                         VOID, DARK_E, ORB_HI, PURPLE, PURP_SH, PURP_MD, PURP_HI,
                         CYAN, GREEN, GREEN_DK, GREEN_PALE, RED, SMOKE, SMOKE_DK,
                         OUTLINE, LABEL, TRACE, P)

CW, CH = 190, 120
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


BASE, SCAN_L, BLIP_L = Layer(CW, CH), Layer(CW, CH), Layer(CW, CH)

# Main frame
frame(BASE, 6, 6, 183, 114, PURPLE, cut=3)
for x in range(10, 180):
    BASE.put(x, 112, PURP_SH)
for y in range(10, 111):
    BASE.put(181, y, PURP_SH)

# Tab
fill(BASE, 12, 2, 66, 12, DARK_E)
frame(BASE, 12, 2, 66, 12, PURPLE, cut=1)
text(BASE, 'QUEST LOG', 17, 4, 1, 1, CYAN)

# Left Radar / Sonar Box
rx1, ry1, rx2, ry2 = 12, 17, 52, 107
fill(BASE, rx1, ry1, rx2, ry2, PANEL_BG)
frame(BASE, rx1, ry1, rx2, ry2, PURPLE, cut=2)

cx, cy, cr = 32, 50, 16
for y in range(ry1 + 1, ry2):
    for x in range(rx1 + 1, rx2):
        d = math.hypot(x + .5 - cx, y + .5 - cy)
        if abs(d - cr) < 0.8:
            BASE.put(x, y, PURP_SH)
        elif abs(d - cr * 0.5) < 0.8:
            BASE.put(x, y, DARK_E)
        elif d < 1.5:
            BASE.put(x, y, GREEN)

# Radar crosshairs
for x in range(cx - cr + 2, cx + cr - 1):
    if x != cx:
        BASE.put(x, cy, '#1D1236')
for y in range(cy - cr + 2, cy + cr - 1):
    if y != cy:
        BASE.put(cx, y, '#1D1236')

# Radar status under circle
text(BASE, 'STATUS', 15, 74, 1, 1, LABEL)
text(BASE, 'ACTIVE', 15, 83, 1, 1, GREEN)
text(BASE, '5 OPS', 15, 94, 1, 1, SMOKE)

# Radar blip
for bx, by in [(38, 44), (27, 58), (35, 56)]:
    BLIP_L.put(bx, by, GREEN)
    BLIP_L.put(bx + 1, by, GREEN_PALE)

# Quests listing on the right
quests = [
    ('C/C++ & SYSTEMS CORE', 'STRENGTHENING FUNDAMENTALS', 4, 18),
    ('LINUX INTERNALS & OS', 'EXPLORING KERNEL CONCEPTS', 3, 36),
    ('STM32 FIRMWARE DEV', 'MICROCONTROLLER DRIVERS', 4, 54),
    ('REAL-TIME OS & HW', 'FREERTOS & INTEGRATION', 3, 72),
    ('CONNECTED IOT SYSTEMS', 'CLOUD ARCHITECTURES & MQTT', 3, 90),
]

for title_txt, desc_txt, pips, y in quests:
    # Quest marker icon [>]
    text(BASE, '>', 58, y, 1, 1, GREEN)
    text(BASE, title_txt, 66, y, 1, 1, SMOKE)
    text(BASE, desc_txt, 66, y + 8, 1, 1, LABEL)
    
    # Progress bar on the right edge
    for i in range(5):
        px = 154 + i * 5
        color = GREEN if i < pips else '#2D1452'
        fill(BASE, px, y + 1, px + 3, y + 5, color)


def build(animate):
    an = (lambda s: s) if animate else (lambda s: '')
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CW} {CH}" width="{CW * P}" '
         f'height="{CH * P}" shape-rendering="crispEdges" role="img" '
         f'aria-label="Currently Working On Quest Log for Ain Shamsudheen: C/C++, Linux, STM32, RTOS, IoT.">',
         '<title>Quest Log: Currently Working On</title>',
         f'<rect width="{CW}" height="{CH}" fill="{VOID}"/>', paths(BASE)]

    if animate:
        # Blinking radar blips
        o.append(f'<g>{paths(BLIP_L)}{an(op("1;0.2;1", "0;0.5;1", 1.5))}</g>')
        # Status LED
        o.append(f'<rect x="180" y="8" width="2" height="2" fill="{CYAN}">'
                 f'{an(op("1;0.2", "0;0.5", 1.4))}</rect>')
    else:
        o.append(paths(BLIP_L))
        o.append(f'<rect x="180" y="8" width="2" height="2" fill="{CYAN}"/>')

    o.append('</svg>')
    return ''.join(o)


if __name__ == '__main__':
    os.makedirs('assets', exist_ok=True)
    for name, flag in [('quests.svg', True), ('quests-static.svg', False)]:
        with open(os.path.join('assets', name), 'w') as f:
            f.write(build(flag))
        print('wrote', name, f'({os.path.getsize(os.path.join("assets", name)) // 1024} KB)')

