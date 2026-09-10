"""
Setup script to create a beautiful cat cartoon image matching the calico cat:
- Orange, black, and white fur (calico pattern)
- Big blue/cyan eyes with highlights
- Cute pink nose and smile
- Sitting pose with visible paws
- Floating snow/sparkle particles on gray background
"""

from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
import math
import random


def create_beautiful_cat(size=800):
    """Create a beautiful calico cat cartoon matching the provided image"""
    img = Image.new('RGB', (size, size), (70, 80, 95))  # gray background
    draw = ImageDraw.Draw(img)

    # Add snow/sparkle particles
    random.seed(42)
    for _ in range(120):
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        r = random.choice([1, 1, 2, 2, 3])
        a = random.randint(150, 255)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(a, a, a + 20))

    cx = size // 2
    cy = size // 2 + 20
    scale = size / 800

    # ---- BODY ----
    body_r = int(200 * scale)
    body_y = cy + int(130 * scale)
    # Main body (dark gray/black)
    draw.ellipse([cx - body_r, body_y - body_r, cx + body_r, body_y + body_r],
                 fill=(55, 58, 68), outline=(40, 42, 50), width=3)

    # Belly/chest (white)
    belly_r = int(140 * scale)
    draw.ellipse([cx - belly_r, body_y - int(80 * scale),
                  cx + belly_r, body_y + belly_r],
                 fill=(252, 250, 248))

    # Orange patches on body sides
    draw.ellipse([cx + int(40 * scale), body_y - int(30 * scale),
                  cx + body_r - int(10 * scale), body_y + int(80 * scale)],
                 fill=(245, 168, 60))

    # ---- TAIL (curled on left) ----
    tail_start_x = cx - int(180 * scale)
    tail_start_y = body_y - int(40 * scale)
    # Create curled tail with multiple ellipses
    for i in range(10):
        angle = math.radians(-150 + i * 25)
        tx = tail_start_x + math.cos(angle) * (80 + i * 3) * scale
        ty = tail_start_y + math.sin(angle) * (80 + i * 3) * scale
        tr = int((40 - i * 2.5) * scale)
        if tr > 0:
            draw.ellipse([tx - tr, ty - tr, tx + tr, ty + tr],
                         fill=(50, 53, 62), outline=(38, 40, 48), width=2)

    # ---- FRONT PAWS (white) ----
    paw_r = int(60 * scale)
    # Left paw
    paw1_x = cx - int(70 * scale)
    paw1_y = body_y + int(130 * scale)
    draw.ellipse([paw1_x - paw_r, paw1_y - paw_r, paw1_x + paw_r, paw1_y + paw_r],
                 fill=(252, 250, 248), outline=(220, 216, 210), width=3)
    # Paw pads
    for pad_x in [paw1_x - int(25 * scale), paw1_x, paw1_x + int(25 * scale)]:
        pad_r = int(8 * scale)
        draw.ellipse([pad_x - pad_r, paw1_y + int(15 * scale) - pad_r,
                      pad_x + pad_r, paw1_y + int(15 * scale) + pad_r],
                     fill=(245, 190, 200))

    # Right paw
    paw2_x = cx + int(70 * scale)
    paw2_y = body_y + int(130 * scale)
    draw.ellipse([paw2_x - paw_r, paw2_y - paw_r, paw2_x + paw_r, paw2_y + paw_r],
                 fill=(252, 250, 248), outline=(220, 216, 210), width=3)
    for pad_x in [paw2_x - int(25 * scale), paw2_x, paw2_x + int(25 * scale)]:
        pad_r = int(8 * scale)
        draw.ellipse([pad_x - pad_r, paw2_y + int(15 * scale) - pad_r,
                      pad_x + pad_r, paw2_y + int(15 * scale) + pad_r],
                     fill=(245, 190, 200))

    # ---- HEAD ----
    head_r = int(170 * scale)
    head_y = cy - int(80 * scale)

    # Head base shape (slightly oval)
    draw.ellipse([cx - head_r, head_y - head_r, cx + head_r, head_y + head_r],
                 fill=(252, 250, 248), outline=(220, 216, 210), width=3)

    # ---- EARS ----
    ear_w = int(70 * scale)
    ear_h = int(95 * scale)

    # Left ear (outer - orange)
    ear1_left = cx - head_r + int(15 * scale)
    ear1_right = ear1_left + ear_w
    ear1_bottom = head_y - head_r + int(45 * scale)
    ear1_top = ear1_bottom - ear_h
    draw.polygon([(ear1_left, ear1_bottom),
                  ((ear1_left + ear1_right) // 2 - int(5 * scale), ear1_top),
                  (ear1_right, ear1_bottom - int(5 * scale))],
                 fill=(245, 168, 60), outline=(200, 135, 40), width=3)
    # Left ear inner (pink)
    draw.polygon([(ear1_left + int(18 * scale), ear1_bottom - int(12 * scale)),
                  ((ear1_left + ear1_right) // 2 - int(3 * scale), ear1_top + int(22 * scale)),
                  (ear1_right - int(18 * scale), ear1_bottom - int(18 * scale))],
                 fill=(255, 210, 180))

    # Right ear (outer - black/dark gray)
    ear2_left = cx + head_r - ear_w - int(15 * scale)
    ear2_right = ear2_left + ear_w
    ear2_bottom = head_y - head_r + int(45 * scale)
    ear2_top = ear2_bottom - ear_h
    draw.polygon([(ear2_left, ear2_bottom - int(5 * scale)),
                  ((ear2_left + ear2_right) // 2 + int(5 * scale), ear2_top),
                  (ear2_right, ear2_bottom)],
                 fill=(55, 58, 68), outline=(38, 40, 48), width=3)
    # Right ear inner (pink)
    draw.polygon([(ear2_left + int(18 * scale), ear2_bottom - int(18 * scale)),
                  ((ear2_left + ear2_right) // 2 + int(3 * scale), ear2_top + int(22 * scale)),
                  (ear2_right - int(18 * scale), ear2_bottom - int(12 * scale))],
                 fill=(255, 210, 180))

    # ---- FUR PATCHES ON HEAD ----
    # Orange patch on left side of face
    draw.ellipse([cx - head_r + int(10 * scale), head_y - int(90 * scale),
                  cx - int(30 * scale), head_y + int(60 * scale)],
                 fill=(245, 168, 60))
    # Dark gray/black patch on right top
    draw.ellipse([cx + int(20 * scale), head_y - head_r - int(5 * scale),
                  cx + head_r + int(10 * scale), head_y + int(40 * scale)],
                 fill=(55, 58, 68))
    # Orange eyebrow/top patch right
    draw.ellipse([cx - int(10 * scale), head_y - head_r - int(30 * scale),
                  cx + int(90 * scale), head_y - int(20 * scale)],
                 fill=(245, 168, 60))
    # Dark patch upper left
    draw.ellipse([cx - head_r - int(10 * scale), head_y - int(30 * scale),
                  cx - int(70 * scale), head_y + int(70 * scale)],
                 fill=(55, 58, 68))

    # ---- EYES (Big blue/cyan) ----
    eye_r_x = int(40 * scale)
    eye_r_y = int(50 * scale)
    eye_y = head_y - int(10 * scale)
    eye_offset_x = int(70 * scale)

    def draw_eye(ex, ey, erx, ery):
        # Eye white/glow
        draw.ellipse([ex - erx - int(4 * scale), ey - ery - int(4 * scale),
                      ex + erx + int(4 * scale), ey + ery + int(4 * scale)],
                     fill=(255, 255, 255))
        # Outer iris (dark/black)
        draw.ellipse([ex - erx, ey - ery, ex + erx, ey + ery],
                     fill=(25, 28, 40), outline=(15, 18, 28), width=2)
        # Iris ring (teal/cyan)
        inner_erx = int(erx * 0.8)
        inner_ery = int(ery * 0.8)
        for i in range(12):
            alpha_val = int(40 + i * 12)
            color = (50 + i * 10, 180 + i * 5, 200 + i * 3)
            ir = inner_erx - i * 1
            iry = inner_ery - i * 1
            if ir > 0 and iry > 0:
                draw.ellipse([ex - ir, ey - iry, ex + ir, ey + iry],
                             fill=color)
        # Pupil (vertical slit)
        pw = int(erx * 0.22)
        ph = int(ery * 0.55)
        draw.ellipse([ex - pw, ey - ph, ex + pw, ey + ph], fill=(10, 12, 22))
        # Highlights (big)
        hr_x = int(erx * 0.42)
        hr_y = int(ery * 0.32)
        hx1 = ex - int(erx * 0.32)
        hy1 = ey - int(ery * 0.35)
        draw.ellipse([hx1 - hr_x, hy1 - hr_y, hx1 + hr_x, hy1 + hr_y],
                     fill=(255, 255, 255))
        # Small secondary highlight
        hr2_x = int(erx * 0.18)
        hr2_y = int(ery * 0.18)
        hx2 = ex + int(erx * 0.45)
        hy2 = ey + int(ery * 0.25)
        draw.ellipse([hx2 - hr2_x, hy2 - hr2_y, hx2 + hr2_x, hy2 + hr2_y],
                     fill=(255, 255, 255))
        # Tiny sparkle
        draw.ellipse([hx1 + int(5 * scale) - int(2 * scale),
                      hy1 + int(ery * 0.05) - int(2 * scale),
                      hx1 + int(5 * scale) + int(2 * scale),
                      hy1 + int(ery * 0.05) + int(2 * scale)],
                     fill=(220, 245, 255))

    draw_eye(cx - eye_offset_x, eye_y, eye_r_x, eye_r_y)
    draw_eye(cx + eye_offset_x, eye_y, eye_r_x, eye_r_y)

    # ---- EYELASHES (top, long and cute) ----
    def draw_lashes(ex, ey, side=1):
        for i in range(4):
            angle = math.radians(-100 + i * 20 + (side * 5))
            lash_len = (18 + (0 if i != 1 else 6)) * scale
            start_x = ex + side * int(eye_r_x * 0.5 * math.cos(angle * 0.3))
            start_y = ey - eye_r_y + int(i * 2 * scale)
            end_x = start_x + math.cos(angle) * lash_len * side
            end_y = start_y - math.sin(angle) * lash_len * 0.6
            draw.line([(start_x, start_y), (end_x, end_y)],
                      fill=(25, 20, 35), width=int(2.2 * scale))

    draw_lashes(cx - eye_offset_x, eye_y, side=-1)
    draw_lashes(cx + eye_offset_x, eye_y, side=1)

    # ---- NOSE (pink/orange heart/triangle) ----
    nose_w = int(22 * scale)
    nose_h = int(16 * scale)
    nose_y = head_y + int(55 * scale)
    draw.polygon([(cx, nose_y + nose_h),
                  (cx - nose_w, nose_y - nose_h // 2),
                  (cx + nose_w, nose_y - nose_h // 2)],
                 fill=(255, 110, 80), outline=(220, 85, 60), width=2)
    # Nose highlight
    draw.ellipse([cx - int(8 * scale), nose_y - nose_h // 2 - int(2 * scale),
                  cx + int(2 * scale), nose_y - int(2 * scale)],
                 fill=(255, 180, 160))

    # ---- MOUTH (cute smile) ----
    mouth_top = nose_y + nose_h + int(5 * scale)
    mouth_bottom = mouth_top + int(35 * scale)
    # Left curve
    draw.arc([cx - int(42 * scale), mouth_top - int(5 * scale),
              cx + int(2 * scale), mouth_bottom],
             start=0, end=180, fill=(90, 55, 45), width=int(3.5 * scale))
    # Right curve
    draw.arc([cx - int(2 * scale), mouth_top - int(5 * scale),
              cx + int(42 * scale), mouth_bottom],
             start=0, end=180, fill=(90, 55, 45), width=int(3.5 * scale))

    # ---- CHEEKS (blush) ----
    for cheek_x in [cx - int(110 * scale), cx + int(110 * scale)]:
        cheek_y = head_y + int(70 * scale)
        cheek_r = int(28 * scale)
        # Create gradient blush
        for i in range(10):
            r = cheek_r - i * 2
            a = int(18 - i * 1.8)
            if a > 0 and r > 0:
                blush = Image.new('RGBA', img.size, (0, 0, 0, 0))
                bdraw = ImageDraw.Draw(blush)
                bdraw.ellipse([cheek_x - r, cheek_y - r, cheek_x + r, cheek_y + r],
                              fill=(255, 160, 180, a))
                img = Image.alpha_composite(img.convert('RGBA'), blush).convert('RGB')
                draw = ImageDraw.Draw(img)

    # ---- WHISKERS (long white) ----
    whisker_y1 = head_y + int(50 * scale)
    whisker_y2 = head_y + int(68 * scale)
    whisker_y3 = head_y + int(86 * scale)
    for wy, len_f in [(whisker_y1, 1.0), (whisker_y2, 1.1), (whisker_y3, 0.95)]:
        # Left whiskers
        lx_start = cx - int(55 * scale)
        lx_end = cx - int(55 * scale + 140 * scale * len_f)
        draw.line([(lx_start, wy - int(3 * scale)), (lx_end, wy - int(8 * scale))],
                  fill=(255, 255, 255), width=int(2.2 * scale))
        draw.line([(lx_start, wy), (lx_end - int(10 * scale), wy + int(2 * scale))],
                  fill=(255, 255, 255), width=int(2.2 * scale))
        draw.line([(lx_start, wy + int(3 * scale)), (lx_end - int(20 * scale), wy + int(10 * scale))],
                  fill=(255, 255, 255), width=int(2.2 * scale))
        # Right whiskers
        rx_start = cx + int(55 * scale)
        rx_end = cx + int(55 * scale + 140 * scale * len_f)
        draw.line([(rx_start, wy - int(3 * scale)), (rx_end, wy - int(8 * scale))],
                  fill=(255, 255, 255), width=int(2.2 * scale))
        draw.line([(rx_start, wy), (rx_end + int(10 * scale), wy + int(2 * scale))],
                  fill=(255, 255, 255), width=int(2.2 * scale))
        draw.line([(rx_start, wy + int(3 * scale)), (rx_end + int(20 * scale), wy + int(10 * scale))],
                  fill=(255, 255, 255), width=int(2.2 * scale))

    # ---- CHEST/TUMMY FLUFFY DETAIL ----
    # Add fur tufts around chest
    fluff_colors = [(252, 250, 248), (248, 244, 240), (250, 248, 244)]
    for i in range(8):
        fx = cx - int(120 * scale) + i * int(34 * scale)
        fy = body_y - int(60 * scale)
        fr = int(18 * scale)
        draw.ellipse([fx - fr, fy - fr, fx + fr, fy + fr],
                     fill=fluff_colors[i % 3])

    # ---- GROUND/SURFACE ----
    ground_y = body_y + int(175 * scale)
    # Soft shadow
    shadow = Image.new('RGBA', img.size, (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.ellipse([cx - int(220 * scale), ground_y - int(10 * scale),
                   cx + int(220 * scale), ground_y + int(30 * scale)],
                  fill=(50, 50, 55, 120))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=int(8 * scale)))
    img = Image.alpha_composite(img.convert('RGBA'), shadow).convert('RGB')
    draw = ImageDraw.Draw(img)

    # Surface line/texture (light gray)
    draw.rectangle([0, ground_y, size, size], fill=(195, 198, 202))
    # Soft edge
    edge = Image.new('RGBA', img.size, (0, 0, 0, 0))
    edraw = ImageDraw.Draw(edge)
    for i in range(8):
        a = int(60 - i * 7)
        if a > 0:
            edraw.line([(0, ground_y + i), (size, ground_y + i)],
                       fill=(120, 120, 130, a), width=1)
    img = Image.alpha_composite(img.convert('RGBA'), edge).convert('RGB')
    draw = ImageDraw.Draw(img)

    # ---- EXTRA SPARKLES ----
    for _ in range(15):
        sx = random.randint(int(50 * scale), size - int(50 * scale))
        sy = random.randint(int(50 * scale), ground_y - int(50 * scale))
        sr = random.choice([2, 3])
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                     fill=(255, 255, 255, 200) if False else (255, 255, 255))

    # Apply subtle softening filter for polished look
    img = img.filter(ImageFilter.SMOOTH_MORE)

    return img


def setup_cat_image():
    output_file = Path("cat_image.png")
    print("🐱 Creating beautiful calico cat image...")
    print("   (Matching the cute cartoon cat you provided!)")

    try:
        # Check if user has a source image
        for src in ["cat_source.png", "cat_source.jpg", "cat_source.jpeg"]:
            src_path = Path(src)
            if src_path.exists():
                print(f"📷 Found source image: {src}")
                from PIL import Image as PILImage
                img = PILImage.open(src_path)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                max_size = 800
                if max(img.size) > max_size:
                    img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                img.save(output_file, 'PNG', optimize=True)
                print(f"✅ Saved user image to: {output_file}")
                return True

        # Generate beautiful cat image
        print("🎨 Generating beautiful cartoon cat...")
        img = create_beautiful_cat(size=800)
        img.save(output_file, 'PNG', optimize=True)
        print(f"✅ Cat image saved to: {output_file}")
        print(f"📏 Size: {img.size}")
        print("")
        print("🐱 Cat features:")
        print("   • Calico pattern (orange/black/white fur)")
        print("   • Big blue/cyan eyes with sparkles")
        print("   • Cute pink nose and smile")
        print("   • Long white whiskers")
        print("   • Fluffy chest and visible paws")
        print("   • Curled dark tail")
        print("   • Sparkle particles in background")
        print("")
        print("🚀 Now run: python siya_floating.py")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("🐱 SIYA CAT IMAGE SETUP 🐱")
    print("=" * 50)
    print()
    ok = setup_cat_image()
    if not ok:
        print("\n💡 Don't worry! siya_floating.py will still work!")
        print("   It will create an automatic placeholder.")
    print()
    try:
        input("Press Enter to exit...")
    except:
        pass
