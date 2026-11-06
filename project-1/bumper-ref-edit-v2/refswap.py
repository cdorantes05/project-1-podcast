# Swap the photo and the note text inside reference-bumper.mp4, keeping everything that passes over them
# (the pointer, the WordPad window fading in and covering them).
# out = frame + (1 - a) * (new - plate), where plate is the clean median background and a is occluder opacity.
import subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi

src, still, out, text = sys.argv[1:5]
W, H, FPS = 1280, 720, 24
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
frames = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
N = len(frames)
plate = np.median(frames[0:140:2].astype(np.float32), 0)

# --- new content ---
PX0, PY0, PX1, PY1 = 697, 63, 1207, 357           # photo rect in Paint
TX0, TY0, TX1, TY1 = 934, 455, 1241, 484           # note text band
img = Image.open(still).convert('RGB')
pw, ph = PX1 - PX0, PY1 - PY0
s = max(pw / img.width, ph / img.height)
img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
l, t = (img.width - pw) // 2, (img.height - ph) // 2
photo = np.asarray(img.crop((l, t, l + pw, t + ph))).astype(np.float32)

# text drawn at 4x then downsampled, monospace with the reference's ~8.9 px pitch
SC = 4
tw, th = TX1 - TX0, TY1 - TY0
canvas = Image.new('L', (tw * SC, th * SC), 255)
d = ImageDraw.Draw(canvas)
font = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', 15 * SC)
pitch = 8.9 * SC
x0, base = (941 - TX0) * SC, (474 - TY0) * SC
for i, ch in enumerate(text + '|'):
    d.text((x0 + i * pitch, base), ch, font=font, fill=0, anchor='ls')
txt = np.asarray(canvas.resize((tw, th), Image.LANCZOS)).astype(np.float32)
new_text = np.repeat(txt[..., None], 3, 2)

# WordPad's white page (fixed position; it fades in over frames ~145-151): the still fit to its width, centred
PG0, PG1, PGT, PGB = 247, 1017, 114, 639
WP_PAGE = (slice(150, 600), slice(300, 900))  # sample area for the fade opacity
iw = PG1 - PG0; ih = round(iw * 9 / 16)
it = PGT + (PGB - PGT - ih) // 2
WP_IMG = (PG0, it, PG1, it + ih)
src_img = Image.open(still).convert('RGB')
s2 = max(iw / src_img.width, ih / src_img.height)
wi = src_img.resize((round(src_img.width * s2), round(src_img.height * s2)), Image.LANCZOS)
l2, t2 = (wi.width - iw) // 2, (wi.height - ih) // 2
wp_still = np.asarray(wi.crop((l2, t2, l2 + iw, t2 + ih))).astype(np.float32)

regions = [  # (x0, y0, x1, y1, new pixels, rows used to estimate the big window's opacity)
    (PX0, PY0, PX1, PY1, np.full_like(photo, 255), slice(PY0, PY1)),   # Paint canvas left blank
    (TX0, TY0, TX1, TY1, new_text, np.r_[404:419, TY0:TY1]),   # notepad title bar (dark blue) + the old text strokes
]

def col_alpha(f, x0, x1, rows):
    pl = plate[rows, x0:x1]; fr = f[rows, x0:x1].astype(np.float32)
    den = 255 - pl
    ratio = np.where(den > 60, (fr - pl) / np.maximum(den, 1), np.nan)
    a = np.nanmedian(ratio.transpose(1, 0, 2).reshape(x1 - x0, -1), 1)
    return np.clip(np.nan_to_num(a), 0, 1)

ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-framerate', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'medium', '-crf', '15', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
for n in range(N):
    f = frames[n].astype(np.float32)
    o = f.copy()
    for x0, y0, x1, y1, new, rows in regions:
        pl = plate[y0:y1, x0:x1]
        fr = f[y0:y1, x0:x1]
        a = np.zeros((y1 - y0, x1 - x0), np.float32)
        if n >= 140:  # the big window fades in and covers columns from the left
            ac = col_alpha(f, x0, x1, rows)
            ac[ac < 0.12] = 0   # keep the real opacity while it fades in, so the new content fades with it
            ac[ac > 0.97] = 1
            if ((ac > 0.15) & (ac < 0.85)).sum() < 8:   # not fading: only the window's border is fractional
                ac = (ac > 0.3).astype(np.float32)
                ac = ndi.binary_dilation(ac > 0, iterations=1).astype(np.float32)
            a[:] = ac[None, :]
        # pointer and anything else that differs from what's expected
        expect = a[..., None] * 255 + (1 - a[..., None]) * pl
        m = np.abs(fr - expect).max(2) > 45
        m = ndi.binary_fill_holes(ndi.binary_closing(m, iterations=2))
        lab, k = ndi.label(m)
        if k:
            sizes = ndi.sum(m, lab, range(1, k + 1))
            m = np.isin(lab, 1 + np.where(sizes >= 25)[0])
        m = ndi.binary_dilation(m, iterations=2)
        if n < 140:  # after this the pointer stays down by the taskbar, below both regions
            a = np.maximum(a, m.astype(np.float32))
        res = np.where(a[..., None] == 0, new, fr + (1 - a[..., None]) * (new - pl))
        if n < 140 and m.any():
            # inside the pointer mask: keep the arrow's own white/black pixels, apply its shadow/antialiasing as darkening
            arrow = (np.abs(fr - pl).max(2) > 45) & ((fr.min(2) > 200) | (fr.max(2) < 70))
            shade = new * np.clip(fr / np.maximum(pl, 1), 0, 1)
            res = np.where((m & arrow)[..., None], fr, np.where(m[..., None], shade, res))
        o[y0:y1, x0:x1] = res
    # the still on WordPad's white page, fading in with the window (o = a*255 + (1-a)*under, so swap the 255 for the still)
    if n >= 144:
        bx0, by0, bx1, by1 = WP_IMG
        reg = (slice(by0, by1), slice(bx0, bx1))
        den = 255 - plate[WP_PAGE]
        r = ((f[WP_PAGE] - plate[WP_PAGE]) / np.maximum(den, 1))[den > 60]
        wa = float(np.clip(np.median(r), 0, 1)) if r.size else 1.0
        wa = 0.0 if wa < 0.1 else (1.0 if wa > 0.98 else wa)
        if wa > 0:
            expect = wa * 255 + (1 - wa) * plate[reg]
            ptr = ndi.binary_dilation(np.abs(f[reg] - expect).max(2) > 45, iterations=2)  # pointer, if it's over the page
            o[reg] = np.where(ptr[..., None], o[reg], o[reg] + wa * (wp_still - 255))
    ff.stdin.write(np.clip(o, 0, 255).astype(np.uint8).tobytes())
ff.stdin.close(); ff.wait()
print(out, N, 'frames')
