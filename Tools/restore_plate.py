"""Copy the real number plate from a source photo into an AI-relit version of it
(free, local). Finds the plate area with SIFT feature matching around the plate,
warps the sharp plate patch into place and matches it to the new light.

Usage:
  python -I Tools/restore_plate.py SRC.jpg RELIT.jpg OUT.jpg x0,y0,x1,y1 [--ctx 3.0]
  The box is the plate in SRC pixels (a little margin is fine).
"""
import argparse

import cv2
import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("relit"); ap.add_argument("out"); ap.add_argument("box")
    ap.add_argument("--ctx", type=float, default=3.0, help="feature search area, in plate sizes")
    ap.add_argument("--debug")
    a = ap.parse_args()

    src, dst = cv2.imread(a.src), cv2.imread(a.relit)
    x0, y0, x1, y1 = map(int, a.box.split(","))
    bw, bh = x1 - x0, y1 - y0
    cx0, cy0 = max(0, int(x0 - bw * a.ctx)), max(0, int(y0 - bh * a.ctx))
    cx1, cy1 = min(src.shape[1], int(x1 + bw * a.ctx)), min(src.shape[0], int(y1 + bh * a.ctx))

    sift = cv2.SIFT_create(8000)
    g1 = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    g2 = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    m1 = np.zeros_like(g1); m1[cy0:cy1, cx0:cx1] = 255
    m1[y0:y1, x0:x1] = 0  # plate itself is blurred in the relit image, skip it
    k1, d1 = sift.detectAndCompute(g1, m1)
    # scale relit into source-size space for consistent matching
    k2, d2 = sift.detectAndCompute(g2, None)
    matches = cv2.BFMatcher().knnMatch(d1, d2, k=2)
    good = [m for m, n in matches if m.distance < 0.75 * n.distance]
    p1 = np.float32([k1[m.queryIdx].pt for m in good])
    p2 = np.float32([k2[m.trainIdx].pt for m in good])
    H, inl = cv2.findHomography(p1, p2, cv2.RANSAC, 4.0)
    print(f"matches {len(good)} inliers {int(inl.sum()) if inl is not None else 0}")

    # Warp the whole source; take only the plate area
    warped = cv2.warpPerspective(src, H, (dst.shape[1], dst.shape[0]), flags=cv2.INTER_LANCZOS4)
    mask = np.zeros(src.shape[:2], np.float32); mask[y0:y1, x0:x1] = 1
    wm = cv2.warpPerspective(mask, H, (dst.shape[1], dst.shape[0]))
    feather = max(2, int(0.06 * min(bw, bh) * abs(np.linalg.det(H[:2, :2])) ** 0.5))
    wm = cv2.GaussianBlur(cv2.erode(wm, np.ones((3, 3))), (0, 0), feather)[..., None]

    # Light match inside the plate area (LAB mean shift, mild contrast match)
    sel = wm[..., 0] > 0.5
    lw = cv2.cvtColor(warped, cv2.COLOR_BGR2LAB).astype(np.float32)
    ld = cv2.cvtColor(dst, cv2.COLOR_BGR2LAB).astype(np.float32)
    for c in range(3):
        ms, md = lw[..., c][sel].mean(), ld[..., c][sel].mean()
        k = 0.6 if c == 0 else 0.8
        lw[..., c] = (lw[..., c] - ms) + ms + (md - ms) * k
    warped = cv2.cvtColor(np.clip(lw, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR).astype(np.float32)

    out = warped * wm + dst.astype(np.float32) * (1 - wm)
    cv2.imwrite(a.out, np.clip(out, 0, 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 93])
    if a.debug:
        ys, xs = np.where(sel)
        pad = 60
        crop = out[max(ys.min() - pad, 0):ys.max() + pad, max(xs.min() - pad, 0):xs.max() + pad]
        cv2.imwrite(a.debug, crop.astype(np.uint8))


if __name__ == "__main__":
    main()
