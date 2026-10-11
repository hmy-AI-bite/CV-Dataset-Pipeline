import os
import cv2
import csv
def is_valid_image(file_name, file_path):
    import re
    valid_exts = ('.png', '.jpg', '.jpeg')
    pattern = re.compile(r'^[a-zA-Z0-9_\-\s\.]+$')

    if not file_name.lower().endswith(valid_exts):
        return False
    if not pattern.match(file_name):
        return False
    if os.path.getsize(file_path) < 1024:
        return False
    return True
# 数据包路径
raw_dir = r"D:\CV-Datatext-Pipeline\library_dataset\images_raw\datasets_for_silk"
# 支持类型
valid_exts = ('.png', '.jpg', '.jpeg')
#输出路径
clean_dir = r"D:\CV-Datatext-Pipeline\library_dataset\images_cleaned\datasets_for_silk"
#定义统一的图像尺寸
target_size = (512, 512)
os.makedirs(clean_dir, exist_ok=True)
count = 1
files_name = os.listdir(raw_dir)
mapping_data = []
#过滤文件
for file_name in files_name:
    if not file_name.lower().endswith(valid_exts):
        continue
    if file_name.startswith("、"): continue
    if not is_valid_image(file_name, os.path.join(raw_dir, file_name)):
        continue
    img = cv2.imread(os.path.join(raw_dir, file_name))
    if img is None:
        print(f"读取失败（可能损坏）：{file_name}")
        continue
    #统一图像尺寸
    img_resized = cv2.resize(img, target_size)
    #保存清理后的图像
    new_file_name = f"silk_{count:04d}.png"
    save_path = os.path.join(clean_dir, new_file_name)
    cv2.imwrite(save_path, img_resized)

    mapping_data.append({"original_name": file_name, "new_name": new_file_name})
    print(f"已保存：{new_file_name}，原始文件名：{file_name}")
    count += 1

#保存映射关系到CSV文件
mapping_csv_path = os.path.join(clean_dir, "mapping.csv")
with open(mapping_csv_path, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["original_name", "new_name"])
    writer.writeheader()
    writer.writerows(mapping_data)
    print("映射关系已保存到 mapping.csv")
print("\n======== 清理完成 ====")
