import os
import cv2
import numpy as np
#数据包路径
data_dir = r"D:\CV-Datatext-Pipeline\library_dataset\images_raw\datasets_for_silk"
#支持类型
valid_exts = ('.png', '.jpg', '.jpeg')

print("开始扫描数据...")
#os.listdir() 方法用于返回指定的文件夹包含的文件或文件夹的名字的列表。
file_names = os.listdir(data_dir)
images_info = []
bad_files = []

for filename in file_names:
    #filename.lower() 将文件名转换为小写，以便进行不区分大小写的比较。
    #endswith() 方法用于检查字符串是否以指定的后缀结尾。
    if not filename.lower().endswith(valid_exts):
        continue
    #os.path.join() 方法用于将多个路径组合后返回。
    file_path = os.path.join(data_dir, filename)
    #cv2.imread() 方法用于读取图像文件，并将其作为 NumPy 数组返回。
    img = cv2.imread(file_path)

    if img is None:
        bad_files.append(filename)
        print(f"读取失败（可能损坏）：{filename}")
    else:
        h,w,c=img.shape
        images_info.append((filename, w, h, c))
        print(f"读取成功：{filename}，宽度：{w}，高度：{h}，通道数：{c}")

print("\n======== 扫描结果 ====")
print(f"总文件数：{len(file_names)}")
print(f"有效图像文件数：{len(images_info)}")
print(f"损坏或无法读取的文件数：{len(bad_files)}")

if images_info:
    widths = [info[1] for info in images_info]
    heights = [info[2] for info in images_info]
    channels = [info[3] for info in images_info]

    print(f"图像宽度范围：{min(widths)} - {max(widths)}")
    print(f"图像高度范围：{min(heights)} - {max(heights)}")
    print(f"图像通道数范围：{min(channels)} - {max(channels)}")

    channels = set(info[3] for info in images_info)
    print(f"图像通道数分布：{channels}(3表示RGB，1表示灰度)")