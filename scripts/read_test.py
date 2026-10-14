import os
import csv
import cv2

csv_path = r"D:\CV-Datatext-Pipeline\library_dataset\images_cleaned\datasets_for_silk\mapping.csv"
old_to_new = {}

with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        old_to_new[row["original_name"]] = row["new_name"]

print(f"字典里映射的键值对数量: {len(old_to_new)}")
print(f"字典里映射的键值对示例: {list(old_to_new.items())[:5]}")  # 打印前5个键值对