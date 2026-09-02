import os
import struct
import zlib

os.makedirs('assets', exist_ok=True)


def chunk(tag, data):
    return struct.pack('!I', len(data)) + tag + data + struct.pack('!I', zlib.crc32(tag + data) & 0xffffffff)


def write_png(path, width, height, color_fn):
    rows = bytearray()
    for y in range(height):
        rows.append(0)
        for x in range(width):
            rows.extend(color_fn(x, y))
    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', struct.pack('!IIBBBBB', width, height, 8, 2, 0, 0, 0))
    png += chunk(b'IDAT', zlib.compress(bytes(rows)))
    png += chunk(b'IEND', b'')
    with open(path, 'wb') as f:
        f.write(png)


def logo_color(x, y):
    if 96 <= x <= 416 and 96 <= y <= 416:
        return (20, 115, 232, 255)
    if 140 <= x <= 372 and 140 <= y <= 372:
        return (255, 255, 255, 230)
    # invoice lines
    if 182 <= x <= 330 and y == 220:
        return (20, 115, 232, 255)
    if 182 <= x <= 294 and y == 258:
        return (20, 115, 232, 255)
    if 182 <= x <= 322 and y == 296:
        return (20, 115, 232, 255)
    if 182 <= x <= 270 and y == 334:
        return (20, 115, 232, 255)
    # backdrop gradient
    return (220 + (y // 4) % 30, 232 + (y // 5) % 20, 255, 255)


def screenshot_color(base_bg, x, y):
    if 130 <= x <= 950 and 90 <= y <= 1830:
        return (18, 26, 39, 255)
    if 175 <= x <= 905 and 150 <= y <= 1770:
        return (250, 252, 255, 255)
    if 200 <= x <= 880 and 190 <= y <= 300:
        return (242, 245, 250, 255)
    if 230 <= x <= 850 and 360 <= y <= 760:
        return (30, 115, 232, 255)
    if 230 <= x <= 510 and 830 <= y <= 1060:
        return (236, 244, 255, 255)
    if 560 <= x <= 850 and 830 <= y <= 1060:
        return (220, 246, 239, 255)
    if 235 <= x <= 845 and 1480 <= y <= 1660:
        return (246, 249, 255, 255)
    if 220 <= x <= 400 and 220 <= y <= 270:
        return (224, 234, 255, 255)
    if 430 <= x <= 600 and 220 <= y <= 270:
        return (224, 234, 255, 255)
    if 630 <= x <= 800 and 220 <= y <= 270:
        return (224, 234, 255, 255)
    if 270 <= x <= 570 and y in {520, 570, 620, 670}:
        return (255, 255, 255, 210)
    if 270 <= x <= 430 and y in {930, 990, 1040}:
        return (20, 115, 232, 180)
    if 620 <= x <= 780 and y in {930, 990}:
        return (31, 171, 127, 180)
    if 270 <= x <= 560 and y in {1520, 1580, 1640}:
        return (120, 133, 163, 180)
    if 650 <= x <= 780 and y in {1520, 1580, 1640}:
        return (20, 115, 232, 200)
    if 740 <= x <= 835 and 1650 <= y <= 1745 and ((x - 787.5) ** 2 + (y - 1697.5) ** 2) <= 47 ** 2:
        return (27, 196, 162, 255)
    return base_bg + (255,)


write_png('assets/logo.png', 512, 512, logo_color)
for name, bg in [
    ('screenshot-1.png', (233, 240, 255)),
    ('screenshot-2.png', (237, 247, 243)),
    ('screenshot-3.png', (248, 243, 255)),
]:
    write_png('assets/' + name, 1080, 1920, lambda x, y, bg=bg: screenshot_color(bg, x, y))

print('Created assets/logo.png and app screenshots in assets/')
