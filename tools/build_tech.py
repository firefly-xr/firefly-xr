#!/usr/bin/env python3
"""
build_tech.py: Technologies & Tools / Arsenal screen.
Reuses the palette, font, and frame styling from build_title.py and build_card.py.

    python build_tech.py -> assets/tech.svg / assets/tech-static.svg
"""
import os
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


BASE, LED_L, TXRX_L = Layer(CW, CH), Layer(CW, CH), Layer(CW, CH)

# Main frame
frame(BASE, 6, 6, 183, 114, PURPLE, cut=3)
for x in range(10, 180):
    BASE.put(x, 112, PURP_SH)
for y in range(10, 111):
    BASE.put(181, y, PURP_SH)

# Tab
fill(BASE, 12, 2, 64, 12, DARK_E)
frame(BASE, 12, 2, 64, 12, PURPLE, cut=1)
text(BASE, 'ARSENAL', 17, 4, 1, 1, CYAN)

# Left Side: Microcontroller chip graphic box
mx1, my1, mx2, my2 = 12, 17, 52, 107
fill(BASE, mx1, my1, mx2, my2, PANEL_BG)
frame(BASE, mx1, my1, mx2, my2, PURPLE, cut=2)

# MCU Chip body (centered around x=32, y=48)
cx1, cy1, cx2, cy2 = 21, 35, 43, 61
fill(BASE, cx1, cy1, cx2, cy2, '#21103A')
frame(BASE, cx1, cy1, cx2, cy2, PURP_MD, cut=1)

# Chip pin 1 notch
BASE.put(cx1 + 2, cy1 + 2, PURP_SH)

# Chip Pins (top & bottom)
for px in range(cx1 + 3, cx2 - 2, 3):
    BASE.put(px, cy1 - 2, SMOKE_DK)
    BASE.put(px, cy1 - 1, SMOKE)
    BASE.put(px, cy2 + 1, SMOKE)
    BASE.put(px, cy2 + 2, SMOKE_DK)

# Chip Pins (left & right)
for py in range(cy1 + 3, cy2 - 2, 3):
    BASE.put(cx1 - 2, py, SMOKE_DK)
    BASE.put(cx1 - 1, py, SMOKE)
    BASE.put(cx2 + 1, py, SMOKE)
    BASE.put(cx2 + 2, py, SMOKE_DK)

# Etched label on chip
text(BASE, 'STM', 24, 41, 1, 1, SMOKE_DK)
text(BASE, '32', 27, 49, 1, 1, CYAN)

# Sub labels below chip
text(BASE, 'ARM-M', 18, 72, 1, 1, LABEL)
text(BASE, 'FREERTOS', 14, 82, 1, 1, GREEN)
text(BASE, 'SYSTEM', 17, 93, 1, 1, SMOKE)

# Blinking TX/RX activity LEDs on PCB
TXRX_L.put(16, 23, GREEN)
TXRX_L.put(16, 24, GREEN)
TXRX_L.put(20, 23, CYAN)
TXRX_L.put(20, 24, CYAN)

# Right Side: Arsenal Categories
categories = [
    ('LANGUAGES', 'C / C++ / PYTHON', CYAN, 18),
    ('EMBEDDED', 'STM32 / ARM / FREERTOS', GREEN, 36),
    ('SYSTEMS', 'LINUX / GIT / GCC / GDB', PURP_HI, 54),
    ('NETWORKING', 'TCP/IP / MQTT / UART / SPI / I2C', CYAN, 72),
    ('CLOUD & INFRA', 'AWS / DOCKER', GREEN, 90),
]

for cat_title, items_str, col, y in categories:
    # Category header
    text(BASE, cat_title, 60, y, 1, 1, col)
    # Category values
    text(BASE, items_str, 60, y + 9, 1, 1, SMOKE)
    # Bottom subtle divider line
    for dx in range(60, 178, 2):
        BASE.put(dx, y + 16, '#1F1138')


def build(animate):
    an = (lambda s: s) if animate else (lambda s: '')
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CW} {CH}" width="{CW * P}" '
         f'height="{CH * P}" shape-rendering="crispEdges" role="img" '
         f'aria-label="Technologies and Tools screen for Ain Shamsudheen: Languages, Embedded, Systems, Networking, Cloud.">',
         '<title>Arsenal: Technologies and Tools</title>',
         f'<rect width="{CW}" height="{CH}" fill="{VOID}"/>', paths(BASE)]

    if animate:
        # Alternating TX/RX LED flicker
        o.append(f'<g>{paths(TXRX_L)}{an(op("1;0.1;0.8;0", "0;0.25;0.6;0.85", 0.8))}</g>')
        # Chip corner heartbeat
        o.append(f'<rect x="180" y="8" width="2" height="2" fill="{PURP_HI}">'
                 f'{an(op("1;0.2", "0;0.5", 1.2))}</rect>')
    else:
        o.append(paths(TXRX_L))
        o.append(f'<rect x="180" y="8" width="2" height="2" fill="{PURP_HI}"/>')

    o.append('</svg>')
    return ''.join(o)


if __name__ == '__main__':
    os.makedirs('assets', exist_ok=True)
    for name, flag in [('tech.svg', True), ('tech-static.svg', False)]:
        with open(os.path.join('assets', name), 'w') as f:
            f.write(build(flag))
        print('wrote', name, f'({os.path.getsize(os.path.join("assets", name)) // 1024} KB)')

