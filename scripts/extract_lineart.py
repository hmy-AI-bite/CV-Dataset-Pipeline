import os
import numpy as np
import cv2

img_dir = r"D:\CV-Datatext-Pipeline\library_dataset\images_cleaned\datasets_for_silk"
output_dir = r"D:\CV-Datatext-Pipeline\library_dataset\images_lineart\datasets_for_silk"
os.makedirs(output_dir, exist_ok=True)
files = os.listdir(img_dir)
count = 0
for file in files:
    if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
        continue
    img_path = os.path.join(img_dir, file)
    img = cv2.imread(img_path)
    if img is None:
        print(f"读取失败（可能损坏）：{file}")
        continue

    # 转为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 方案 A：原始灰度图 + 轻度平滑
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    edges_a = cv2.Canny(blurred, 30, 80)
    lineart_a = cv2.bitwise_not(edges_a)

    cv2.imwrite(
        os.path.join(output_dir, f"{file}"), lineart_a
    )
    print(f"已处理：{file}")
