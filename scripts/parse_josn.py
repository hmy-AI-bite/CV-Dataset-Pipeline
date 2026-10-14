import json
import numpy as np
import cv2
json_path = r"D:\CV-Datatext-Pipeline\library_dataset\annotations_json\project-1-at-2026-10-10-17-16-87ec2f90.json"

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)
    first = data[0]
    annotations = first["annotations"]
    result = annotations[0]["result"]
    value = result[0]["value"]
    points = value["points"]
    pixel_points = []
    for point in points:
        x_pixel = int(point[0] * 512 / 100)
        y_pixel = int(point[1] * 512 / 100)
        pixel_points.append((x_pixel, y_pixel))
    print(f"像素点个数: {len(pixel_points)}")
    mask = np.zeros((512, 512), dtype=np.uint8)
    pts_array = np.array(pixel_points, dtype=np.int32)
    cv2.fillPoly(mask, [pts_array], 255)
    cv2.imwrite(r"D:\CV-Datatext-Pipeline\library_dataset\mask\mask_test.png", mask)