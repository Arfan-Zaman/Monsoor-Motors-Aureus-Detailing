"""Put a real stock-car cutout (Higgsfield image_background_remover PNG) onto
the empty Monsoor yard plate. The car's shape, paint and condition are kept;
only a light warmth match, a ground shadow and an optional plate blur are added.

Usage:
  python -I Tools/car_yard_composite.py PLATE CUT.png OUT.jpg W H [--width 0.78] [--blur x0,y0,x1,y1 ...]
  W H = output size (e.g. 2000 1500 or 1500 1875). Blur boxes are in the cutout's pixels.
"""
import argparse

import cv2
import numpy as np


def cover(img, w, h, focus_x=0.42, focus_y=0.5):
    s = max(w / img.shape[1], h / img.shape[0])
    r = cv2.resize(img, (round(img.shape[1] * s), round(img.shape[0] * s)), interpolation=cv2.INTER_AREA)
    x = int((r.shape[1] - w) * focus_x)
    y = int((r.shape[0] - h) * focus_y)
    return r[y:y + h, x:x + w]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plate"); ap.add_argument("cut"); ap.add_argument("out")
    ap.add_argument("W", type=int); ap.add_argument("H", type=int)
    ap.add_argument("--width", type=float, default=0.78, help="car width as share of frame")
    ap.add_argument("--bottom", type=float, default=0.93, help="tyre line as share of frame height")
    ap.add_argument("--blur", nargs="*", default=[])
    ap.add_argument("--warm", type=float, default=0.35)
    a = ap.parse_args()

    W, H = a.W, a.H
    bg = cover(cv2.imread(a.plate), W, H).astype(np.float32)

    cut = cv2.imread(a.cut, cv2.IMREAD_UNCHANGED)
    rgb, al = cut[..., :3].copy(), cut[..., 3]
    for b in a.blur:
        x0, y0, x1, y1 = map(int, b.split(","))
        rgb[y0:y1, x0:x1] = cv2.GaussianBlur(rgb[y0:y1, x0:x1], (0, 0), 14)
    ys, xs = np.where(al > 20)
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    touch_l, touch_r = x0 <= 2, x1 >= cut.shape[1] - 3
    touch_b = y1 >= cut.shape[0] - 3
    rgb, al = rgb[y0:y1 + 1, x0:x1 + 1], al[y0:y1 + 1, x0:x1 + 1]

    # Scale the car
    s = a.width * W / rgb.shape[1]
    if rgb.shape[0] * s > 0.80 * H:
        s = 0.80 * H / rgb.shape[0]
    cw, ch = round(rgb.shape[1] * s), round(rgb.shape[0] * s)
    rgb = cv2.resize(rgb, (cw, ch), interpolation=cv2.INTER_AREA)
    al = cv2.resize(al, (cw, ch), interpolation=cv2.INTER_AREA).astype(np.float32) / 255

    # Position: centred, tyres on the bay; a car cut by the original frame stays on that edge
    px = (W - cw) // 2
    if touch_l:
        px = 0
    elif touch_r:
        px = W - cw
    py = H - ch if touch_b else int(a.bottom * H) - ch

    # Light match: pull the car part-way toward the yard's warm tone (LAB a/b means only)
    car = rgb.astype(np.float32)
    lab_c = cv2.cvtColor(rgb, cv2.COLOR_BGR2LAB).astype(np.float32)
    ground = bg[int(H * 0.7):, :].astype(np.uint8)
    lab_g = cv2.cvtColor(ground, cv2.COLOR_BGR2LAB).astype(np.float32)
    m = al > 0.5
    for ch_i in (1, 2):
        shift = (lab_g[..., ch_i].mean() - lab_c[..., ch_i][m].mean()) * a.warm * 0.4
        lab_c[..., ch_i] += shift
    car = cv2.cvtColor(np.clip(lab_c, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR).astype(np.float32)

    # Shadow: soft wide pool + tight contact shadow along the bottom of the car
    shadow = np.zeros((H, W), np.float32)
    full = np.zeros((H, W), np.float32)
    yy0, yy1 = max(py, 0), min(py + ch, H)
    full[yy0:yy1, px:px + cw] = al[yy0 - py:yy1 - py]
    bottom_rows = np.zeros_like(full)
    cols = np.where(full.max(axis=0) > 0.5)[0]
    for c in cols:
        r = np.where(full[:, c] > 0.5)[0]
        if len(r):
            yb = r.max()
            bottom_rows[max(yb - 6, 0):min(yb + 4, H), c] = 1
    pool = cv2.GaussianBlur(bottom_rows, (0, 0), 0.035 * W)
    pool = cv2.dilate(pool, np.ones((1, int(0.02 * W)), np.uint8))
    contact = cv2.GaussianBlur(bottom_rows, (0, 0), 0.006 * W)
    shadow = np.clip(pool / max(pool.max(), 1e-6) * 0.55 + contact / max(contact.max(), 1e-6) * 0.6, 0, 0.85)
    out = bg * (1 - shadow[..., None])

    # Composite
    region = out[yy0:yy1, px:px + cw]
    aa = al[yy0 - py:yy1 - py, :, None]
    region[:] = car[yy0 - py:yy1 - py] * aa + region * (1 - aa)
    cv2.imwrite(a.out, np.clip(out, 0, 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 93])
    print(a.out, W, H)


if __name__ == "__main__":
    main()
