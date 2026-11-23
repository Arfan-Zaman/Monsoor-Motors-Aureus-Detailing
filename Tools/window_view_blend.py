"""Keep a real interior photo, take only the window views from an AI edit (free, local).

The AI edit (e.g. gpt_image_2_6 "replace the view through the windows") is aligned to the
real photo with SIFT, then only the areas that changed a lot (the windows) are blended in.
Seats, wear and trims stay the real pixels.

Usage:
  python -I Tools/window_view_blend.py REAL.jpg AI.png OUT.jpg [--thresh 38] [--preview P.jpg]
"""
import argparse

import cv2
import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("real"); ap.add_argument("ai"); ap.add_argument("out")
    ap.add_argument("--thresh", type=float, default=38)
    ap.add_argument("--preview")
    a = ap.parse_args()
    o = cv2.imread(a.real)
    ai = cv2.resize(cv2.imread(a.ai), (o.shape[1], o.shape[0]), interpolation=cv2.INTER_AREA)
    sift = cv2.SIFT_create(6000)
    k1, d1 = sift.detectAndCompute(cv2.cvtColor(ai, cv2.COLOR_BGR2GRAY), None)
    k2, d2 = sift.detectAndCompute(cv2.cvtColor(o, cv2.COLOR_BGR2GRAY), None)
    m = [x for x, y in cv2.BFMatcher().knnMatch(d1, d2, k=2) if x.distance < 0.7 * y.distance]
    H, inl = cv2.findHomography(np.float32([k1[x.queryIdx].pt for x in m]),
                                np.float32([k2[x.trainIdx].pt for x in m]), cv2.RANSAC, 3.0)
    ai = cv2.warpPerspective(ai, H, (o.shape[1], o.shape[0]), borderMode=cv2.BORDER_REPLICATE)
    diff = np.abs(cv2.GaussianBlur(ai, (0, 0), 5).astype(np.float32)
                  - cv2.GaussianBlur(o, (0, 0), 5).astype(np.float32)).max(axis=2)
    mk = (diff > a.thresh).astype(np.uint8)
    mk = cv2.morphologyEx(mk, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
    mk = cv2.morphologyEx(mk, cv2.MORPH_CLOSE, np.ones((31, 31), np.uint8))
    nl, lab, st, _ = cv2.connectedComponentsWithStats(mk)
    keep = np.zeros_like(mk)
    for i in range(1, nl):
        if st[i, 4] > 0.004 * mk.size:
            keep[lab == i] = 1
    keep = cv2.dilate(keep, np.ones((7, 7), np.uint8))
    w = cv2.GaussianBlur(keep.astype(np.float32), (0, 0), 4)[..., None]
    out = (ai * w + o * (1 - w)).astype(np.uint8)
    cv2.imwrite(a.out, out, [cv2.IMWRITE_JPEG_QUALITY, 93])
    print(a.out, f"inliers {int(inl.sum())}/{len(m)}", f"window share {keep.mean() * 100:.1f}%")
    if a.preview:
        h = 420
        s = lambda x: cv2.resize(x, (int(x.shape[1] * h / x.shape[0]), h))
        mv = cv2.cvtColor((keep * 255).astype(np.uint8), cv2.COLOR_GRAY2BGR)
        cv2.imwrite(a.preview, np.hstack([s(o), s(mv), s(out)]))


if __name__ == "__main__":
    main()
