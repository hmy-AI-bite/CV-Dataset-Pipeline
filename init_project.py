import os

def create_structure():
    base = "library_dataset"
    folders = [
        "images_raw",      # 存放图书馆拍的原图
        "images_cleaned",  # 存放清洗后的图
        "annotations_json",# 存放标注生成的JSON
        "visualizations",  # 存放画框校验的图
        "scripts"          # 你的Python代码
    ]
    for folder in folders:
        path = os.path.join(base, folder)
        os.makedirs(path, exist_ok=True)
        print(f"创建成功: {path}")

if __name__ == "__main__":
    create_structure()
    print("项目脚手架搭建完成！")