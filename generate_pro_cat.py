"""
Siya Pro Cat Image Generator
Creates 15+ transparent-calico cat expressions exactly matching the reference image:
  - Calico fur (orange/black/white patches in exact positions)
  - Big blue/cyan eyes with two-white-dot highlights
  - Visible toe lines on front paws
  - Curled dark tail on left
  - Fluffy fur rendering with layered strands
  - Proper shading matching reference lighting (top-left light)
All output PNGs have alpha channel (true transparency - NO BACKGROUND BOX).
"""

from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from pathlib import Path
import math
import random


FUR_WHITE = (250, 248, 244)
FUR_WHITE_SHADOW = (225, 220, 212)
FUR_ORANGE = (242, 165, 55)
FUR_ORANGE_SHADOW = (205, 135, 40)
FUR_DARK = (52, 55, 64)
FUR_DARK_SHADOW = (35, 38, 46)
SKIN_PINK = (255, 210, 185)
NOSE_PINK = (255, 118, 85)
NOSE_DARK = (220, 90, 65)
EYE_WHITE = (255, 255, 255)
EYE_OUTLINE = (18, 20, 28)
IRIS_OUTER = (45, 175, 195)
IRIS_MID = (70, 150, 170)
PUPIL = (10, 12, 22)
MOUTH_LINE = (92, 58, 46)
WHISKER = (255, 255, 255)
GROUND_SHADOW = (40, 40, 46)
PAW_PAD = (245, 195, 205)


def _soft_blur(alpha_img, radius=2):
    return alpha_img.filter(ImageFilter.GaussianBlur(radius=radius))


def _fur_tufts(base_img, cx, cy, radii_range, color, count=25, seed=42):
    """Draw fine fur tuft lines around a circle for fluff effect"""
    rnd = random.Random(seed)
    overlay = Image.new('RGBA', base_img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for _ in range(count):
        angle = rnd.uniform(0, math.tau)
        dist = rnd.uniform(radii_range[0], radii_range[1])
        length = rnd.uniform(8, 22)
        x1 = cx + math.cos(angle) * dist
        y1 = cy + math.sin(angle) * dist
        outward_angle = angle + rnd.uniform(-0.4, 0.4)
        x2 = x1 + math.cos(outward_angle) * length
        y2 = y1 + math.sin(outward_angle) * length
        lw = rnd.choice([1, 1, 2])
        a = rnd.randint(70, 140)
        od.line([(x1, y1), (x2, y2)], fill=(*color, a), width=lw)
    return Image.alpha_composite(base_img, overlay)


def draw_base_cat(size=800, variant="normal"):
    """Draw the cat with expression variant, returns RGBA with alpha"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx = size // 2
    cy = size // 2 + 30
    S = size / 800.0

    # ========== GROUND SOFT SHADOW ==========
    shadow = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    gy = cy + int(265 * S)
    sd.ellipse([cx - int(240 * S), gy - int(18 * S),
                cx + int(240 * S), gy + int(30 * S)],
               fill=(*GROUND_SHADOW, 130))
    shadow = _soft_blur(shadow, int(10 * S))
    img = Image.alpha_composite(img, shadow)
    draw = ImageDraw.Draw(img)

    # ========== TAIL (curled on LEFT, dark) ==========
    tail_layers = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    td = ImageDraw.Draw(tail_layers)
    tail_cx = cx - int(200 * S)
    tail_cy = cy + int(110 * S)
    for i, (r, sc) in enumerate(zip(
            [int(95 * S), int(85 * S), int(72 * S), int(62 * S), int(52 * S),
             int(44 * S), int(36 * S), int(28 * S), int(22 * S)],
            [FUR_DARK_SHADOW] + [FUR_DARK] * 6 + [FUR_DARK_SHADOW] * 2)):
        angle = math.radians(-160 + i * 22)
        rr = r
        tx = tail_cx + math.cos(angle) * (90 + i * 4) * S
        ty = tail_cy + math.sin(angle) * (90 + i * 4) * S
        td.ellipse([tx - rr, ty - rr, tx + rr, ty + rr], fill=(*sc, 255))
    # Little orange accent inside tail curl base
    td.ellipse([tail_cx - int(50 * S), tail_cy - int(20 * S),
                tail_cx - int(5 * S), tail_cy + int(55 * S)],
               fill=(*FUR_ORANGE, 255))
    tail_layers = _soft_blur(tail_layers, 1)
    img = Image.alpha_composite(img, tail_layers)
    draw = ImageDraw.Draw(img)

    # ========== BODY (calico pattern with orange side patches & dark outer) ==========
    body_cy = cy + int(165 * S)
    body_rx = int(215 * S)
    body_ry = int(195 * S)
    # Outer dark (sides)
    draw.ellipse([cx - body_rx, body_cy - body_ry, cx + body_rx, body_cy + body_ry],
                 fill=(*FUR_DARK, 255))
    # White belly (center) - taller vertically
    belly_rx = int(150 * S)
    belly_ry = int(165 * S)
    draw.ellipse([cx - belly_rx, body_cy - int(95 * S),
                  cx + belly_rx, body_cy + belly_ry - int(20 * S)],
                 fill=(*FUR_WHITE, 255))
    # Orange right-side body patch (matches ref: viewer right, cat's left)
    op_cx = cx + int(115 * S)
    op_cy = body_cy + int(15 * S)
    op_rx = int(80 * S)
    op_ry = int(110 * S)
    draw.ellipse([op_cx - op_rx, op_cy - op_ry, op_cx + op_rx, op_cy + op_ry],
                 fill=(*FUR_ORANGE, 255))
    # Dark left body side (viewer left) - reinforce
    dp_cx = cx - int(150 * S)
    dp_cy = body_cy + int(10 * S)
    dp_rx = int(60 * S)
    dp_ry = int(140 * S)
    draw.ellipse([dp_cx - dp_rx, dp_cy - dp_ry, dp_cx + dp_rx, dp_cy + dp_ry],
                 fill=(*FUR_DARK, 255))

    # ========== FRONT PAWS (white, with toe lines & pink pads) ==========
    def draw_paw(px, py, toe_shift=0):
        pr = int(62 * S)
        # Paw main (rounded)
        draw.ellipse([px - pr, py - int(pr * 0.85), px + pr, py + pr],
                     fill=(*FUR_WHITE, 255))
        # Toe separation lines (3 divisions = 4 toes as in ref)
        toe_y = py - int(5 * S)
        for dx in [-int(28 * S), -int(8 * S), int(12 * S), int(30 * S)]:
            draw.ellipse([px + dx - int(6 * S), toe_y - int(10 * S),
                          px + dx + int(6 * S), toe_y + int(3 * S)],
                         fill=(*FUR_WHITE_SHADOW, 180))
        # Toe outline lines (shallow arcs)
        for dx in [-int(25 * S), 0, int(25 * S)]:
            draw.arc([px + dx - int(18 * S), toe_y - int(16 * S),
                      px + dx + int(18 * S), toe_y + int(6 * S)],
                     start=10, end=170, fill=(*FUR_WHITE_SHADOW, 200), width=max(1, int(1.5 * S)))
        # Bottom pads (underneath - not too visible)
        pad_col = (*PAW_PAD, 230)
        pad_y = py + int(25 * S)
        for pad_dx in [-int(20 * S), int(2 * S), int(22 * S)]:
            pad_r = int(7 * S)
            draw.ellipse([px + pad_dx - pad_r, pad_y - pad_r,
                          px + pad_dx + pad_r, pad_y + pad_r], fill=pad_col)

    paw1_x = cx - int(72 * S)
    paw1_y = body_cy + int(165 * S)
    paw2_x = cx + int(72 * S)
    paw2_y = body_cy + int(165 * S)
    draw_paw(paw1_x, paw1_y)
    draw_paw(paw2_x, paw2_y)

    # ========== CHEST FLUFF (white tufts above body meeting head) ==========
    chest_y = body_cy - int(80 * S)
    for dx in range(-3, 4):
        tx = cx + dx * int(36 * S)
        ty = chest_y + (0 if dx % 2 == 0 else int(-12 * S))
        tr = int(20 * S)
        draw.ellipse([tx - tr, ty - tr, tx + tr, ty + tr], fill=(*FUR_WHITE, 255))

    # ========== HEAD (white base, add calico patches) ==========
    head_cy = cy - int(80 * S)
    h_rx = int(175 * S)
    h_ry = int(165 * S)
    draw.ellipse([cx - h_rx, head_cy - h_ry, cx + h_rx, head_cy + h_ry],
                 fill=(*FUR_WHITE, 255))

    # --- CALICO HEAD PATCHES (exact ref positions) ---
    # 1) Orange on LEFT (viewer left, cat's right): covers left ear down cheek
    op_h_cx = cx - int(95 * S)
    op_h_cy = head_cy - int(10 * S)
    draw.ellipse([op_h_cx - int(110 * S), op_h_cy - int(130 * S),
                  op_h_cx + int(70 * S), op_h_cy + int(90 * S)],
                 fill=(*FUR_ORANGE, 255))
    # 2) Dark (black-gray) on RIGHT upper (viewer right, cat's left)
    dp_h_cx = cx + int(100 * S)
    dp_h_cy = head_cy - int(55 * S)
    draw.ellipse([dp_h_cx - int(75 * S), dp_h_cy - int(115 * S),
                  dp_h_cx + int(105 * S), dp_h_cy + int(80 * S)],
                 fill=(*FUR_DARK, 255))
    # 3) Orange forehead top-right blaze between ears
    fop_cx = cx + int(15 * S)
    fop_cy = head_cy - int(130 * S)
    draw.ellipse([fop_cx - int(90 * S), fop_cy - int(55 * S),
                  fop_cx + int(85 * S), fop_cy + int(35 * S)],
                 fill=(*FUR_ORANGE, 255))
    # 4) Dark eyebrow/corner on left upper
    fdp_cx = cx - int(90 * S)
    fdp_cy = head_cy - int(55 * S)
    draw.ellipse([fdp_cx - int(70 * S), fdp_cy - int(60 * S),
                  fdp_cx + int(25 * S), fdp_cy + int(60 * S)],
                 fill=(*FUR_DARK, 255))
    # 5) White blaze center (brighten middle forehead) - reinforces white
    draw.ellipse([cx - int(55 * S), head_cy - int(155 * S),
                  cx + int(45 * S), head_cy - int(30 * S)],
                 fill=(*FUR_WHITE, 255))

    # ========== EARS ==========
    # Left ear (viewer left, cat's right) — ORANGE outside
    ear_lx0 = cx - h_rx + int(18 * S)
    ear_lx1 = cx - h_rx + int(90 * S)
    ear_ly0 = head_cy - h_ry + int(45 * S)
    ear_ly1 = head_cy - h_ry - int(95 * S)
    draw.polygon([
        (ear_lx0, ear_ly0),
        ((ear_lx0 + ear_lx1) // 2 - int(3 * S), ear_ly1),
        (ear_lx1, ear_ly0 - int(5 * S)),
    ], fill=(*FUR_ORANGE, 255), outline=(*FUR_ORANGE_SHADOW, 255), width=max(1, int(2 * S)))
    # Left inner pink
    draw.polygon([
        (ear_lx0 + int(20 * S), ear_ly0 - int(15 * S)),
        ((ear_lx0 + ear_lx1) // 2 - int(2 * S), ear_ly1 + int(25 * S)),
        (ear_lx1 - int(20 * S), ear_ly0 - int(20 * S)),
    ], fill=(*SKIN_PINK, 255))

    # Right ear (viewer right, cat's left) — DARK outside
    ear_rx0 = cx + h_rx - int(90 * S)
    ear_rx1 = cx + h_rx - int(18 * S)
    ear_ry0 = head_cy - h_ry + int(45 * S)
    ear_ry1 = head_cy - h_ry - int(95 * S)
    draw.polygon([
        (ear_rx0, ear_ry0 - int(5 * S)),
        ((ear_rx0 + ear_rx1) // 2 + int(3 * S), ear_ry1),
        (ear_rx1, ear_ry0),
    ], fill=(*FUR_DARK, 255), outline=(*FUR_DARK_SHADOW, 255), width=max(1, int(2 * S)))
    # Right inner pink
    draw.polygon([
        (ear_rx0 + int(20 * S), ear_ry0 - int(20 * S)),
        ((ear_rx0 + ear_rx1) // 2 + int(2 * S), ear_ry1 + int(25 * S)),
        (ear_rx1 - int(20 * S), ear_ry0 - int(15 * S)),
    ], fill=(*SKIN_PINK, 255))

    # Ear fur tufts
    img = _fur_tufts(img, (ear_lx0 + ear_lx1) // 2, (ear_ly1 + ear_ly0) // 2,
                     (int(10 * S), int(45 * S)), FUR_ORANGE, count=12, seed=11)
    img = _fur_tufts(img, (ear_rx0 + ear_rx1) // 2, (ear_ry1 + ear_ry0) // 2,
                     (int(10 * S), int(45 * S)), FUR_DARK, count=12, seed=12)
    draw = ImageDraw.Draw(img)

    # ========== EYES ==========
    eye_y = head_cy - int(12 * S)
    eye_gap = int(75 * S)
    eye_rx = int(42 * S)
    eye_ry = int(52 * S)

    def draw_eye(ex, ey, erx, ery, var=variant):
        # Sclera bright white
        draw.ellipse([ex - erx - int(4 * S), ey - ery - int(4 * S),
                      ex + erx + int(4 * S), ey + ery + int(4 * S)],
                     fill=(*EYE_WHITE, 255))
        # Outer eye outline (dark)
        draw.ellipse([ex - erx, ey - ery, ex + erx, ey + ery],
                     fill=(*EYE_OUTLINE, 255), outline=(*EYE_OUTLINE, 255), width=max(1, int(2 * S)))
        # Iris gradient rings (cyan → teal, 8 layers)
        for i in range(10):
            shade = (IRIS_OUTER[0] - i * 2, IRIS_OUTER[1] + i * 4, IRIS_OUTER[2] - i * 2)
            ir_x = int(erx * 0.82) - i * max(1, int(2.2 * S))
            ir_y = int(ery * 0.82) - i * max(1, int(2.2 * S))
            if ir_x > 2 and ir_y > 2:
                draw.ellipse([ex - ir_x, ey - ir_y, ex + ir_x, ey + ir_y], fill=(*shade, 255))
        # Inner dark pupil ring after iris layers
        prx = int(erx * 0.5)
        pry = int(ery * 0.65)
        draw.ellipse([ex - prx, ey - pry, ex + prx, ey + pry], fill=(*EYE_OUTLINE, 255))

        if var in ("closed", "sleepy", "blink"):
            # Closed eye: draw a curved lid line
            lw = max(2, int(3 * S))
            draw.ellipse([ex - erx, ey - ery, ex + erx, ey + ery],
                         fill=(*EYE_OUTLINE, 255))  # cover with outline color
            # Lid skin-tone band for half-open in sleepy
            if var == "sleepy":
                draw.ellipse([ex - erx, ey - ery, ex + erx, ey], fill=(*FUR_WHITE_SHADOW, 255))
                draw.arc([ex - erx + int(8 * S), ey - int(ery * 0.3),
                          ex + erx - int(8 * S), ey + int(ery * 0.1)],
                         start=10, end=170, fill=(*EYE_OUTLINE, 255), width=lw)
            else:
                draw.arc([ex - erx + int(6 * S), ey - ery + int(8 * S),
                          ex + erx - int(6 * S), ey + ery - int(8 * S)],
                         start=10, end=170, fill=(*EYE_OUTLINE, 255), width=lw)
        else:
            # Pupil shape
            if var == "surprised":
                pwx = int(erx * 0.32)
                pwy = int(ery * 0.45)
            elif var == "happy":
                pwx = int(erx * 0.24)
                pwy = int(ery * 0.58)
            elif var == "angry":
                pwx = int(erx * 0.2)
                pwy = int(ery * 0.65)
            else:  # normal, thinking, loving, excited, etc.
                pwx = int(erx * 0.23)
                pwy = int(ery * 0.56)
            draw.ellipse([ex - pwx, ey - pwy, ex + pwx, ey + pwy], fill=(*PUPIL, 255))

            # Two white highlights (exact reference style: big + small)
            hl1_rx = int(erx * 0.43)
            hl1_ry = int(ery * 0.33)
            hl1_x = ex - int(erx * 0.33)
            hl1_y = ey - int(ery * 0.36)
            draw.ellipse([hl1_x - hl1_rx, hl1_y - hl1_ry, hl1_x + hl1_rx, hl1_y + hl1_ry],
                         fill=(255, 255, 255, 255))
            hl2_r = int(erx * 0.2)
            hl2_x = ex + int(erx * 0.45)
            hl2_y = ey + int(ery * 0.26)
            draw.ellipse([hl2_x - hl2_r, hl2_y - hl2_r, hl2_x + hl2_r, hl2_y + hl2_r],
                         fill=(255, 255, 255, 255))
            # Tiny sparkle
            if var in ("excited", "loving", "happy"):
                spark_r = max(1, int(2 * S))
                draw.ellipse([hl1_x + int(5 * S) - spark_r, hl1_y + int(3 * S) - spark_r,
                              hl1_x + int(5 * S) + spark_r, hl1_y + int(3 * S) + spark_r],
                             fill=(235, 250, 255, 255))

    draw_eye(cx - eye_gap, eye_y, eye_rx, eye_ry)
    draw_eye(cx + eye_gap, eye_y, eye_rx, eye_ry)

    # ========== EYELASHES ==========
    lash_count = 4
    for side_sign, ex in [(-1, cx - eye_gap), (1, cx + eye_gap)]:
        for i in range(lash_count):
            t = (i + 0.5) / lash_count
            ox = int(eye_rx * 0.5)
            oy = -int(eye_ry * 0.85) + int(i * 3 * S)
            lash_len = (18 + (3 if i == 1 or i == 2 else 0)) * S
            angle = math.radians(-85 + t * 40)
            start_x = ex + side_sign * ox
            start_y = eye_y + oy
            end_x = start_x + math.cos(angle) * lash_len * side_sign
            end_y = start_y - math.sin(angle) * lash_len * 0.55
            lw = max(1, int(2.2 * S))
            draw.line([(start_x, start_y), (end_x, end_y)], fill=(*EYE_OUTLINE, 255), width=lw)

    # ========== EYEBROW VARIANTS (happy / angry / surprised) ==========
    if variant == "angry":
        lw = max(2, int(3.5 * S))
        # Angled V-down to center brows
        for side_sign, ex in [(-1, cx - eye_gap), (1, cx + eye_gap)]:
            bx = ex - side_sign * int(20 * S)
            by = eye_y - int(eye_ry) - int(15 * S)
            bx2 = ex + side_sign * int(30 * S)
            by2 = eye_y - int(eye_ry) - int(28 * S)
            draw.line([(bx - side_sign * int(30 * S), by), (bx2, by2)],
                      fill=(*EYE_OUTLINE, 230), width=lw)
    elif variant == "happy":
        lw = max(2, int(3 * S))
        for side_sign, ex in [(-1, cx - eye_gap), (1, cx + eye_gap)]:
            sx = ex - int(35 * S)
            sy = eye_y - int(eye_ry) - int(18 * S)
            ex2 = ex + int(35 * S)
            ey2 = eye_y - int(eye_ry) - int(10 * S)
            draw.arc([sx, sy - int(5 * S), ex2, ey2 + int(20 * S)], start=10, end=170,
                     fill=(*EYE_OUTLINE, 180), width=lw)
    elif variant == "surprised":
        lw = max(2, int(3 * S))
        for side_sign, ex in [(-1, cx - eye_gap), (1, cx + eye_gap)]:
            sx = ex - int(35 * S)
            sy = eye_y - int(eye_ry) - int(28 * S)
            ex2 = ex + int(35 * S)
            ey2 = eye_y - int(eye_ry) - int(15 * S)
            draw.arc([sx, sy - int(5 * S), ex2, ey2 + int(10 * S)], start=190, end=350,
                     fill=(*EYE_OUTLINE, 180), width=lw)

    # ========== NOSE (pink/orange heart-triangle) ==========
    nw = int(24 * S)
    nh = int(18 * S)
    nose_y = head_cy + int(58 * S)
    draw.polygon([
        (cx, nose_y + nh),
        (cx - nw, nose_y - nh // 2),
        (cx + nw, nose_y - nh // 2),
    ], fill=(*NOSE_PINK, 255), outline=(*NOSE_DARK, 255), width=max(1, int(2 * S)))
    # Shine highlight
    draw.ellipse([cx - int(10 * S), nose_y - nh // 2,
                  cx + int(2 * S), nose_y - int(1 * S)],
                 fill=(255, 195, 175, 255))

    # ========== MOUTH ==========
    mouth_top = nose_y + nh + int(3 * S)
    mouth_bot = mouth_top + int(32 * S)
    if variant in ("happy", "excited", "loving"):
        # Bigger smile
        arc_r = int(46 * S)
        draw.arc([cx - arc_r, mouth_top - int(10 * S), cx + int(5 * S), mouth_bot + int(5 * S)],
                 start=10, end=175, fill=(*MOUTH_LINE, 255), width=max(1, int(3.5 * S)))
        draw.arc([cx - int(5 * S), mouth_top - int(10 * S), cx + arc_r, mouth_bot + int(5 * S)],
                 start=5, end=170, fill=(*MOUTH_LINE, 255), width=max(1, int(3.5 * S)))
    elif variant in ("sad", "crying"):
        # Frown
        arc_r = int(40 * S)
        draw.arc([cx - arc_r, mouth_top + int(5 * S), cx + int(5 * S), mouth_bot + int(20 * S)],
                 start=195, end=350, fill=(*MOUTH_LINE, 255), width=max(1, int(3 * S)))
        draw.arc([cx - int(5 * S), mouth_top + int(5 * S), cx + arc_r, mouth_bot + int(20 * S)],
                 start=190, end=345, fill=(*MOUTH_LINE, 255), width=max(1, int(3 * S)))
    elif variant == "surprised":
        # Small O mouth
        om_r = int(14 * S)
        omy = mouth_top + int(10 * S)
        draw.ellipse([cx - om_r, omy - om_r, cx + om_r, omy + om_r],
                     fill=(140, 85, 72, 255), outline=(*MOUTH_LINE, 255), width=max(1, int(2 * S)))
    elif variant == "playful":
        # Tongue out
        arc_r = int(42 * S)
        draw.arc([cx - arc_r, mouth_top - int(8 * S), cx + int(5 * S), mouth_bot + int(3 * S)],
                 start=10, end=175, fill=(*MOUTH_LINE, 255), width=max(1, int(3.2 * S)))
        draw.arc([cx - int(5 * S), mouth_top - int(8 * S), cx + arc_r, mouth_bot + int(3 * S)],
                 start=5, end=170, fill=(*MOUTH_LINE, 255), width=max(1, int(3.2 * S)))
        # Pink tongue below smile
        tgx = int(18 * S)
        tgy = int(16 * S)
        tcy = mouth_bot + int(5 * S)
        draw.ellipse([cx - tgx, tcy - tgy, cx + tgx, tcy + tgy],
                     fill=(255, 145, 165, 255))
    else:
        # Normal gentle smile
        arc_r = int(40 * S)
        draw.arc([cx - arc_r, mouth_top - int(5 * S), cx + int(5 * S), mouth_bot],
                 start=15, end=170, fill=(*MOUTH_LINE, 255), width=max(1, int(3.2 * S)))
        draw.arc([cx - int(5 * S), mouth_top - int(5 * S), cx + arc_r, mouth_bot],
                 start=10, end=165, fill=(*MOUTH_LINE, 255), width=max(1, int(3.2 * S)))

    # ========== CHEEK BLUSH (conditional) ==========
    if variant in ("happy", "shy", "loving", "excited"):
        blush = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        bd = ImageDraw.Draw(blush)
        for cheek_x in [cx - int(112 * S), cx + int(112 * S)]:
            cheek_y = head_cy + int(72 * S)
            cr = int(28 * S)
            for layer in range(6):
                r = cr - layer * max(1, int(3.5 * S))
                a = max(5, 40 - layer * 6)
                if r > 1:
                    bd.ellipse([cheek_x - r, cheek_y - r, cheek_x + r, cheek_y + r],
                               fill=(255, 155, 180, a))
        blush = _soft_blur(blush, max(1, int(3 * S)))
        img = Image.alpha_composite(img, blush)
        draw = ImageDraw.Draw(img)

    # ========== TEARS (crying variant) ==========
    if variant == "crying":
        tears = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        td2 = ImageDraw.Draw(tears)
        for sign in [-1, 1]:
            tx = cx + sign * int(75 * S)
            ty = eye_y + int(25 * S)
            # Single teardrop shape
            td2.ellipse([tx - int(8 * S), ty - int(10 * S), tx + int(8 * S), ty + int(22 * S)],
                        fill=(120, 200, 255, 230))
            # Highlight shine on tear
            td2.ellipse([tx - int(3 * S), ty - int(5 * S), tx + int(1 * S), ty + int(2 * S)],
                        fill=(220, 245, 255, 255))
        tears = _soft_blur(tears, 1)
        img = Image.alpha_composite(img, tears)
        draw = ImageDraw.Draw(img)

    # ========== HEARTS OVERLAY (loving variant) ==========
    if variant == "loving":
        hearts_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        hd = ImageDraw.Draw(hearts_img)

        def draw_heart(hx, hy, hr, color):
            # Two circles + triangle
            hd.ellipse([hx - hr, hy - hr, hx, hy], fill=color)
            hd.ellipse([hx, hy - hr, hx + hr, hy], fill=color)
            hd.polygon([(hx - hr, hy - int(hr * 0.2)),
                        (hx + hr, hy - int(hr * 0.2)),
                        (hx, hy + hr)], fill=color)

        positions = [
            (cx - int(150 * S), head_cy - int(180 * S), int(16 * S), (255, 80, 130, 230)),
            (cx + int(150 * S), head_cy - int(150 * S), int(14 * S), (255, 100, 150, 220)),
            (cx + int(10 * S), head_cy - int(210 * S), int(11 * S), (255, 120, 170, 210)),
            (cx - int(90 * S), head_cy - int(220 * S), int(9 * S), (255, 140, 180, 200)),
            (cx + int(180 * S), head_cy - int(60 * S), int(10 * S), (255, 110, 160, 215)),
            (cx - int(200 * S), head_cy - int(40 * S), int(8 * S), (255, 90, 140, 225)),
        ]
        for hx, hy, hr, col in positions:
            draw_heart(hx, hy, hr, col)
        img = Image.alpha_composite(img, hearts_img)
        draw = ImageDraw.Draw(img)

    # ========== STARS / SPARKLES (excited variant) ==========
    if variant == "excited":
        stars = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        sd2 = ImageDraw.Draw(stars)

        def draw_star(sx, sy, sr, col):
            points = []
            for i in range(10):
                r = sr if i % 2 == 0 else sr * 0.45
                a = math.radians(-90 + i * 36)
                points.append((sx + math.cos(a) * r, sy + math.sin(a) * r))
            sd2.polygon(points, fill=col)

        rnd = random.Random(7)
        for _ in range(12):
            sx = rnd.randint(int(60 * S), int(size - 60 * S))
            sy = rnd.randint(int(40 * S), int(size * 0.7))
            sr = rnd.choice([int(7 * S), int(9 * S), int(12 * S)])
            col = rnd.choice([
                (255, 240, 100, 220), (255, 220, 50, 230),
                (180, 230, 255, 200), (255, 255, 255, 230),
            ])
            draw_star(sx, sy, sr, col)
        stars = _soft_blur(stars, 1)
        img = Image.alpha_composite(img, stars)
        draw = ImageDraw.Draw(img)

    # ========== "ZZZ" (sleepy) ==========
    if variant in ("sleepy", "closed"):
        zimg = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        zd = ImageDraw.Draw(zimg)
        fontsz = max(12, int(28 * S))
        try:
            from PIL import ImageFont
            font = ImageFont.truetype("arial.ttf", fontsz)
        except Exception:
            font = ImageFont.load_default()
        zpos = [(cx + int(110 * S), int(55 * S)),
                (cx + int(150 * S), int(95 * S)),
                (cx + int(185 * S), int(135 * S))]
        zcolors = [(180, 190, 255, 255), (150, 170, 255, 230), (130, 150, 255, 200)]
        for (zx, zy), col, letter in zip(zpos, zcolors, ["z", "Z", "z"]):
            zd.text((zx, zy), letter, fill=col, font=font)
        img = Image.alpha_composite(img, zimg)
        draw = ImageDraw.Draw(img)

    # ========== QUESTION MARK (thinking) ==========
    if variant == "thinking":
        qimg = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        qd = ImageDraw.Draw(qimg)
        fontsz = max(14, int(40 * S))
        try:
            from PIL import ImageFont
            font = ImageFont.truetype("arialbd.ttf", fontsz)
        except Exception:
            try:
                from PIL import ImageFont
                font = ImageFont.truetype("arial.ttf", fontsz)
            except Exception:
                font = ImageFont.load_default()
        # Bubble
        bx, by = cx + int(130 * S), int(70 * S)
        br = int(30 * S)
        qd.ellipse([bx - br, by - br, bx + br, by + br], fill=(255, 255, 255, 245), outline=(180, 180, 200, 2000000))
        # "?" mark inside bubble
        try:
            bbox = font.getbbox("?")
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
        except Exception:
            tw, th = (fontsz // 2, fontsz)
        qd.text((bx - tw / 2, by - th / 2 - 2), "?", fill=(90, 90, 140, 255), font=font)
        # Tiny bubble trail dots
        for i, (tdx, tdy, tr) in enumerate([(int(50 * S), int(60 * S), int(7 * S)),
                                            (int(85 * S), int(105 * S), int(5 * S)),
                                            (int(110 * S), int(140 * S), int(3.5 * S))]):
            qd.ellipse([cx + tdx - tr, head_cy + tdy - tr, cx + tdx + tr, head_cy + tdy + tr],
                       fill=(255, 255, 255, 240 - i * 15), outline=(180, 180, 200, 180 - i * 20), width=1)
        img = Image.alpha_composite(img, qimg)
        draw = ImageDraw.Draw(img)

    # ========== WHISKERS (6 on each side, layered colors) ==========
    def do_whiskers():
        row_ys = [head_cy + int(52 * S), head_cy + int(70 * S), head_cy + int(88 * S)]
        lens_factors = [0.95, 1.1, 1.0]
        widths = [max(1, int(2.5 * S)), max(1, int(2.8 * S)), max(1, int(2.5 * S))]
        for (wy, lf, lw) in zip(row_ys, lens_factors, widths):
            for sign in [-1, 1]:
                xs = cx + sign * int(58 * S)
                xe = cx + sign * int((58 + 155 * lf) * S)
                # 3 slight angled variations per row (ref has 6 total)
                for dy, dxl in [(-int(4 * S), -int(10 * S) * sign),
                                (0, 0),
                                (int(4 * S), int(10 * S) * sign)]:
                    draw.line([(xs, wy + dy), (xe + dxl, wy + dy + int(5 * S))],
                              fill=(*WHISKER, 255), width=lw)
                    # Second whisker slightly offset for 2nd layer of 6 = 12 total
                    draw.line([(xs, wy + dy + int(1 * S)), (xe + dxl - sign * int(8 * S), wy + dy + int(6 * S))],
                              fill=(255, 250, 255, 210), width=max(1, lw - 1))

    do_whiskers()

    # ========== OUTER FUR FLUFF (entire silhouette soft tufts) ==========
    # Head tufts
    img = _fur_tufts(img, cx, head_cy, (int(h_rx * 0.9), int(h_rx * 1.08)),
                     FUR_WHITE, count=30, seed=1)
    img = _fur_tufts(img, cx - int(100 * S), head_cy - int(60 * S), (int(50 * S), int(90 * S)),
                     FUR_ORANGE, count=15, seed=2)
    img = _fur_tufts(img, cx + int(100 * S), head_cy - int(60 * S), (int(50 * S), int(90 * S)),
                     FUR_DARK, count=15, seed=3)
    # Body tufts
    img = _fur_tufts(img, cx, body_cy, (int(body_rx * 0.9), int(body_rx * 1.05)),
                     FUR_WHITE, count=25, seed=4)
    img = _fur_tufts(img, cx + int(110 * S), body_cy, (int(50 * S), int(95 * S)),
                     FUR_ORANGE, count=14, seed=5)
    img = _fur_tufts(img, cx - int(140 * S), body_cy, (int(45 * S), int(85 * S)),
                     FUR_DARK, count=14, seed=6)
    # Belly tufts
    img = _fur_tufts(img, cx, body_cy + int(100 * S), (int(belly_rx * 0.8), int(belly_rx * 0.98)),
                     FUR_WHITE, count=18, seed=7)

    # Final very soft smoothing
    img = img.filter(ImageFilter.SMOOTH)
    return img


ALL_VARIANTS = [
    "normal", "happy", "sleepy", "blink", "closed",
    "thinking", "surprised", "excited", "loving", "shy",
    "angry", "sad", "crying", "playful", "wink"
]


def generate_all(out_dir: Path):
    out_dir.mkdir(exist_ok=True)
    size = 800
    print(f"🎨 Generating {len(ALL_VARIANTS)} cat expressions (size={size}x{size}, transparent PNG)...")
    for v in ALL_VARIANTS:
        img = draw_base_cat(size=size, variant=v)
        path = out_dir / f"cat_{v}.png"
        img.save(path, 'PNG', optimize=True)
        print(f"   ✅ {v:12s} → {path.name} ({path.stat().st_size:,} bytes)")
    # Also make "cat_image.png" = normal (backward compat)
    import shutil
    shutil.copyfile(out_dir / "cat_normal.png", out_dir / "cat_image.png")
    print(f"\n[OK] Done! {len(ALL_VARIANTS) + 1} files in {out_dir.resolve()}")
    print("   (cat_image.png = default normal expression)")


if __name__ == "__main__":
    generate_all(Path("cat_sprites"))
