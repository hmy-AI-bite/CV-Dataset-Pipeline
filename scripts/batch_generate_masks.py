import os
import numpy as np
import cv2
import json
import csv

csv_path = r"D:\CV-Datatext-Pipeline\library_dataset\images_cleaned\datasets_for_silk\mapping.csv"
old_to_new = {}

with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        old_to_new[row["original_name"]] = row["new_name"]

json_path = r"D:\CV-Datatext-Pipeline\library_dataset\annotations_json\project-1-at-2026-10-10-17-16-87ec2f90.json"

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)
    for image in data:
        original_name = image.get("file_upload")  # 用 .get() 更安全，找不到会返回 None 而不是报错
        #测试用例，记得清理
        original_name = "02d686e2797d30619ddb1ea4de055056.jpg"
        if not original_name:
            print("Warning: Image has no file_upload field. Skipping.")
            continue
        try:
            new_name = old_to_new[original_name]
        except KeyError:
            print(f"Warning: {original_name} not found in mapping. Skipping.")
            continue
        annotations = image["annotations"]
        result = annotations[0]["result"]
        value = result[0]["value"]
        points = value["points"]
        pixel_points = []
        for point in points:
            x_pixel = int(point[0] * 512 / 100)
            y_pixel = int(point[1] * 512 / 100)
            pixel_points.append((x_pixel, y_pixel))
        mask = np.zeros((512, 512), dtype=np.uint8)
        pts_array = np.array(pixel_points, dtype=np.int32)
        cv2.fillPoly(mask, [pts_array], 255)
        mask_output_path = os.path.join(r"D:\CV-Datatext-Pipeline\library_dataset\mask", f"{os.path.splitext(new_name)[0]}.png")
        cv2.imwrite(mask_output_path, mask)
        clean_dir = r"D:\CV-Datatext-Pipeline\library_dataset\images_cleaned\datasets_for_silk"
        clean_path = os.path.join(clean_dir, new_name)
        img = cv2.imread(clean_path)


        print(f"Mask saved for {new_name} at {mask_output_path}")