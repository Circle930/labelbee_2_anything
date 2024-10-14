import os

def remove_jpg_from_filenames(input_dir, output_dir):
    """
    循环读取input_dir目录下的所有图片文件,去除文件名中的".jpg",并将结果保存到output_dir目录下。
    """
    # 创建output_dir目录(如果不存在)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历input_dir目录下的所有文件
    for filename in os.listdir(input_dir):
        # 检查文件是否为图片文件
        if filename.endswith(".jpg.png"):
            # 构建输入和输出文件路径
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename.replace(".jpg", ""))

            # 重命名文件
            os.rename(input_path, output_path)
            print(f"Renamed {filename} to {os.path.basename(output_path)}")

# 示例用法
output_dir = "removejpg_output"
input_dir = "/Users/circle/Desktop/Project/Dataset/footdot_data/labelbee"
remove_jpg_from_filenames(input_dir, output_dir)