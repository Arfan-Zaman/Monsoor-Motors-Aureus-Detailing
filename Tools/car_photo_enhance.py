"""Honest sale-photo enhancer for Monsoor Motors car listings.

Fixes light, white balance, contrast, colour and sharpness, and crops to
Facebook-friendly frames (4:3 landscape, 4:5 portrait). It never changes the
car's paint, condition, damage, odometer or warning lights.
Optional: blur a background rectangle (e.g. another dealer's sign).

Usage:
  /opt/miniconda3/bin/python -I Tools/car_photo_enhance.py SRC_DIR OUT_DIR order.json

order.json: [{"src": "5.jpg", "name": "01-Front-Three-Quarter",
              "crop": "bottom|center|top|none", "blur": [[x0,y0,x1,y1], ...]}]
"""
import json
import os
import sys

import cv2
import numpy as np


def white_balance(img, strength=0.6):
    # Gray-world on mid-tones only, blended gently so paint colour stays true.
    f = img.astype(np.float32)
    lum = f.mean(axis=2)
    mask = (lum > 40) & (lum < 220)
    means = f[mask].mean(axis=0)
    gain = means.mean() / means
    gain = 1 + (gain - 1) * strength
    return np.clip(f * gain, 0, 255).astype(np.uint8)


def tone(img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    # Local contrast (lifts shadows on dark paint and interiors, keeps sky)
    clahe = cv2.createCLAHE(clipLimit=1.6, tileGridSize=(8, 8))
    l2 = clahe.apply(l)
    l = cv2.addWeighted(l, 0.45, l2, 0.55, 0)
    # Gentle levels stretch
    lo, hi = np.percentile(l, (0.5, 99.6))
    l = np.clip((l.astype(np.float32) - lo) * 255.0 / max(hi - lo, 1), 0, 255)
    # Soft S-curve
    x = l / 255.0
    x = x + 0.10 * (x - 0.5) * (1 - np.abs(2 * x - 1))
    l = np.clip(x * 255, 0, 255).astype(np.uint8)
    return cv2.cvtColor(cv2.merge([l, a, b]), cv2.COLOR_LAB2BGR)


def vibrance(img, amount=0.18):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
    s = hsv[..., 1] / 255.0
    s = s + amount * s * (1 - s)  # boosts muted colours more than strong ones
    hsv[..., 1] = np.clip(s * 255, 0, 255)
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)


def sharpen(img, amount=0.6, radius=1.4):
    blur = cv2.GaussianBlur(img, (0, 0), radius)
    return cv2.addWeighted(img, 1 + amount, blur, -amount, 0)


def blur_regions(img, boxes):
    out = img.copy()
    for x0, y0, x1, y1 in boxes:
        mask = np.zeros(img.shape[:2], np.float32)
        mask[y0:y1, x0:x1] = 1
        mask = cv2.GaussianBlur(mask, (0, 0), 18)[..., None]
        heavy = cv2.GaussianBlur(img, (0, 0), 22)
        out = (out * (1 - mask) + heavy * mask).astype(np.uint8)
    return out


def crop(img, mode):
    h, w = img.shape[:2]
    if mode == "none":
        return img
    if h > w:  # portrait -> 4:5
        nh = int(w * 5 / 4)
        if nh >= h:
            return img
        y = {"bottom": h - nh, "top": 0, "center": (h - nh) // 2}[mode]
        return img[y:y + nh]
    nw = int(h * 4 / 3)  # landscape -> 4:3
    if nw >= w:
        return img
    x = (w - nw) // 2
    return img[:, x:x + nw]


def process(path, item):
    img = cv2.imread(path)
    if item.get("blur"):
        img = blur_regions(img, item["blur"])
    img = white_balance(img)
    img = tone(img)
    img = vibrance(img)
    img = sharpen(img)
    return crop(img, item.get("crop", "center"))


def main():
    src, out, order = sys.argv[1], sys.argv[2], sys.argv[3]
    os.makedirs(out, exist_ok=True)
    for item in json.load(open(order)):
        res = process(os.path.join(src, item["src"]), item)
        dst = os.path.join(out, item["name"] + ".jpg")
        cv2.imwrite(dst, res, [cv2.IMWRITE_JPEG_QUALITY, 93])
        print(dst, res.shape[1], "x", res.shape[0])


if __name__ == "__main__":
    main()
