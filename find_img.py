import os

def find_and_remove_duplicates(image_folder, json_folder, common_rule):
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

    # 删除没有对应JSON文件的图像文件
    for image_file in image_files - common_files:
        os.remove(os.path.join(image_folder, image_file))

# 自定义共同文件名规则
def custom_common_rule(image_file, json_file):
    return image_file.split(".")[0] in json_file.split(".")[0]

# 指定图像文件夹和JSON文件夹的路径
image_folder = "/Users/circle/Desktop/Project/Dataset/footdot_data/img_tans"  # 替换为图像文件夹的路径
json_folder = "/Users/circle/Desktop/Project/Dataset/footdot_data/labelme"    # 替换为JSON文件夹的路径

# 运行函数以查找和删除重复文件
find_and_remove_duplicates(image_folder, json_folder, custom_common_rule)
