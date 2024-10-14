import os
import shutil

# 查找并复制共同文件
def find_and_copy_duplicates(image_folder, json_folder, common_rule, output_folder):
    # 获取图像文件名集合
    image_files = set(os.listdir(image_folder))

    # 获取JSON文件名集合
    json_files = set(os.listdir(json_folder))

    # 定义共同文件名集合
    common_files = set()

    # 根据规则查找共同文件名
    for image_file in image_files:
        for json_file in json_files:
            if common_rule(image_file, json_file):
                common_files.add(image_file)
                common_files.add(json_file)

    # 创建输出文件夹
    os.makedirs(output_folder, exist_ok=True)

    # 复制共同文件到输出文件夹
    for common_file in common_files:
        if common_file != '.DS_Store':  # 跳过.DS_Store文件
            destination_path = os.path.join(output_folder, common_file)
            if not os.path.exists(destination_path):  # 检查目标文件是否存在
                if common_file in image_files:
                    shutil.copy(os.path.join(image_folder, common_file), output_folder)
                if common_file in json_files:
                    shutil.copy(os.path.join(json_folder, common_file), output_folder)


# 自定义共同文件名规则
def custom_common_rule(image_file, json_file):
    # 提取文件名中 ".json" 前面的子字符串
    image_prefix = image_file
    json_prefix = json_file.split(".json")[0]
    # 比较子字符串是否相同
    return image_prefix == json_prefix



# 指定图像文件夹和JSON文件夹的路径
image_folder = "/Users/circle/Desktop/Project/Dataset/footdot_data/image"  # 替换为图像文件夹的路径
json_folder = "/Users/circle/Desktop/Project/Dataset/footdot_data/result"   # 替换为JSON文件夹的路径

# 指定输出文件夹的路径
output_folder = "/Users/circle/Desktop/Project/Dataset/footdot_data/labelbee"  # 替换为输出文件夹的路径

# 运行函数以查找和复制共同文件
find_and_copy_duplicates(image_folder, json_folder, custom_common_rule, output_folder)
