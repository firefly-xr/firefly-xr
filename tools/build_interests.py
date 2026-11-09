#!/usr/bin/env python3
"""
build_interests.py: Technical Interests / System Domains screen.
Reuses the palette, font, and frame styling from build_title.py and build_card.py.

    python build_interests.py -> assets/interests.svg / assets/interests-static.svg
"""
import os
from build_title import (Layer, paths, text, tr, op,
                         VOID, DARK_E, PURPLE, PURP_SH, PURP_MD, PURP_HI,
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


BASE, PULSE_L, PTR_L = Layer(CW, CH), Layer(CW, CH), Layer(CW, CH)

# Main frame
frame(BASE, 6, 6, 183, 114, PURPLE, cut=3)
for x in range(10, 180):
    BASE.put(x, 112, PURP_SH)
for y in range(10, 111):
    BASE.put(181, y, PURP_SH)

# Tab
fill(BASE, 12, 2, 60, 12, DARK_E)
frame(BASE, 12, 2, 60, 12, PURPLE, cut=1)
text(BASE, 'DOMAINS', 17, 4, 1, 1, CYAN)

# Left architecture stack box
bx1, by1, bx2, by2 = 12, 17, 56, 107
fill(BASE, bx1, by1, bx2, by2, PANEL_BG)
frame(BASE, bx1, by1, bx2, by2, PURPLE, cut=2)

# Layers in the stack box
layers = [
    ('APP', 22, SMOKE_DK, '#221638'),
    ('OS/KERN', 42, PURP_HI, '#2D1452'),
    ('RTOS/FW', 62, CYAN, '#0F3447'),
    ('HARDWARE', 82, GREEN, '#124024'),
]

for label, y, text_col, bg_col in layers:
    fill(BASE, bx1 + 3, y, bx2 - 3, y + 15, bg_col)
    frame(BASE, bx1 + 3, y, bx2 - 3, y + 15, PURP_SH, cut=1)
    text(BASE, label, bx1 + 6, y + 4, 1, 1, text_col)

# Animated pointer / indicator pointing to low level
for y in range(50, 100, 2):
    BASE.put(bx2 + 2, y, TRACE)
text(PTR_L, '>', bx2 + 1, 72, 1, 1, GREEN)

# Right side: Domains list
items = [
    ('SYSTEMS PROGRAMMING', 'C / C++ / LINUX / THREADS', CYAN, 18),
    ('EMBEDDED SYSTEMS', 'STM32 / ARM / FREERTOS', GREEN, 36),
    ('COMPUTER SYSTEMS', 'OS ARCH & LOW-LVL DEBUG', PURP_HI, 54),
    ('NETWORKING', 'TCP/IP / UART / SPI / I2C', CYAN, 72),
    ('CLOUD & INFRA', 'MQTT / AWS / DOCKER', GREEN, 90),
]

for title_txt, sub_txt, col, y in items:
    # Bullet icon
    fill(BASE, 62, y + 2, 64, y + 4, col)
    text(BASE, title_txt, 68, y, 1, 1, col)
    text(BASE, sub_txt, 68, y + 9, 1, 1, SMOKE)


def build(animate):
    an = (lambda s: s) if animate else (lambda s: '')
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CW} {CH}" width="{CW * P}" '
         f'height="{CH * P}" shape-rendering="crispEdges" role="img" '
         f'aria-label="Technical Interests and Domains screen for Ain Shamsudheen: Systems, Embedded, Computer Systems, Networking, Cloud.">',
         '<title>Technical Interests: Systems Domains</title>',
         f'<rect width="{CW}" height="{CH}" fill="{VOID}"/>', paths(BASE)]

    if animate:
        # Blinking cursor/pointer
        o.append(f'<g>{paths(PTR_L)}{an(op("1;0", "0;0.5", 0.9))}</g>')
        # Subtly pulsing power LED
        o.append(f'<rect x="180" y="8" width="2" height="2" fill="{GREEN}">'
                 f'{an(op("1;0.3", "0;0.5", 1.8))}</rect>')
    else:
        o.append(paths(PTR_L))
        o.append(f'<rect x="180" y="8" width="2" height="2" fill="{GREEN}"/>')

    o.append('</svg>')
    return ''.join(o)


if __name__ == '__main__':
    os.makedirs('assets', exist_ok=True)
    for name, flag in [('interests.svg', True), ('interests-static.svg', False)]:
        with open(os.path.join('assets', name), 'w') as f:
            f.write(build(flag))
        print('wrote', name, f'({os.path.getsize(os.path.join("assets", name)) // 1024} KB)')

