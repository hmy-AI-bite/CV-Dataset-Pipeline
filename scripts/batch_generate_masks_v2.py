import os
import csv
import json
import cv2
import numpy as np

BASE = r"D:\CV-Datatext-Pipeline\library_dataset"
CLEAN_DIR = os.path.join(BASE, "images_cleaned", "datasets_for_silk")
MASK_DIR = os.path.join(BASE, "mask")
VIS_DIR = os.path.join(BASE, "visualizations")
CSV_PATH = os.path.join(CLEAN_DIR, "mapping.csv")
JSON_PATH = os.path.join(BASE, "annotations_json",
                         "project-1-at-2026-10-10-17-16-87ec2f90.json")
SIZE = 512

os.makedirs(MASK_DIR, exist_ok=True)
os.makedirs(VIS_DIR, exist_ok=True)

# 1. 读映射表
with open(CSV_PATH, "r", encoding="utf-8") as f:
    old_to_new = {r["original_name"]: r["new_name"] for r in csv.DictReader(f)}

# 2. 读标注
with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

ok, skipped = 0, []

for item in data:
    original_name = item.get("file_upload")
    new_name = old_to_new.get(original_name)
    if new_name is None:
        skipped.append((original_name, "不在 mapping 里"))
        continue

    # 取有效标注(没有被跳过的)
    anns = [a for a in item.get("annotations", []) if not a.get("was_cancelled")]
    if not anns:
        skipped.append((original_name, "没有有效标注"))
        continue

    mask = np.zeros((SIZE, SIZE), dtype=np.uint8)
    n_poly = 0
    for res in anns[0]["result"]:
        if res.get("type") != "polygonlabels":
            continue
        pts = [(int(x * SIZE / 100), int(y * SIZE / 100))
               for x, y in res["value"]["points"]]
        cv2.fillPoly(mask, [np.array(pts, dtype=np.int32)], 255)
        n_poly += 1

    if n_poly == 0:
        skipped.append((original_name, "没有多边形"))
        continue

    stem = os.path.splitext(new_name)[0]
    cv2.imwrite(os.path.join(MASK_DIR, stem + ".png"), mask)

    # 叠加图:把 mask 区域染成红色,半透明
    img = cv2.imread(os.path.join(CLEAN_DIR, new_name))
    overlay = img.copy()
    overlay[mask == 255] = (0, 0, 255)
    vis = cv2.addWeighted(img, 0.6, overlay, 0.4, 0)
    cv2.imwrite(os.path.join(VIS_DIR, stem + "_vis.png"), vis)

    ok += 1
    print(f"{new_name}: {n_poly} 个多边形")

print(f"\n成功 {ok} 张,跳过 {len(skipped)} 张")
for name, reason in skipped:
    print("  跳过:", name, "-", reason)