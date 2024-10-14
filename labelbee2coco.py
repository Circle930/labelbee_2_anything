import json
import os
import shutil
from PIL import Image


def convert_to_coco(labelbee_json_path, image_id, image_width, image_height, start_id=0):
    with open(labelbee_json_path, 'r') as f:
        labelbee_data = json.load(f)

    # 检查是否有必要的字段
    if "step_1" not in labelbee_data or "result" not in labelbee_data["step_1"]:
        print(f"警告：文件 {labelbee_json_path} 中缺少 'step_1' 或 'result' 字段")
        return None  # 如果缺失关键字段则跳过该文件

    coco_annotations = []
    keypoints_list = []  # 存储所有关键点的信息

    # 创建标注信息字典
    annotation_info = {
        "num_keypoints": 12,  # 假设每个点只有一个关键点
        "area": image_width * image_height,  # 整个图像的面积
        "iscrowd": 0,  # 假设每个点都不是群集
        "image_id": image_id,  # 图像ID
        "bbox": [0, 0, image_width, image_height],  # 整个图像作为边界框
        "category_id": 1,  # 假设所有点都属于同一类别
        "id": image_id,  # 每个标注的唯一ID
    }

    # 遍历所有关键点，将每个关键点的坐标和可见性标志添加到列表中
    for point_data in labelbee_data["step_1"]["result"]:
        keypoints_list.extend([int(point_data["x"]), int(point_data["y"]), 2])

    # 检查关键点数量是否正确
    if len(keypoints_list) != 36:  # 每个关键点应该有 12 * 3 = 36 个数值
        print(f"警告：文件 {labelbee_json_path} 中的关键点数量不正确")
        return None

    # 将关键点列表添加到标注信息字典中
    annotation_info["keypoints"] = keypoints_list
    coco_annotations.append(annotation_info)

    return {
        "annotations": coco_annotations,
        "images": [{
            "file_name": os.path.splitext(os.path.basename(labelbee_json_path))[0],
            "height": image_height,
            "width": image_width,
            "id": image_id
        }]
    }


def convert_labelbee_to_paddle(labelbee_dir, output_dir, val_ratio=0.05):
    # 创建必要的文件夹
    train_dir = os.path.join(output_dir, 'train')
    val_dir = os.path.join(output_dir, 'val')
    annotations_dir = os.path.join(output_dir, 'annotations')
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)
    os.makedirs(annotations_dir, exist_ok=True)

    # 初始化 COCO 数据结构
    coco_train = {
        "images": [],
        "annotations": [],
        "categories": [{
            "supercategory": "foot",
            "id": 1,
            "name": "footT",
            "keypoints": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
            "skeleton": []
        }]
    }
    coco_val = {
        "images": [],
        "annotations": [],
        "categories": [{
            "supercategory": "foot",
            "id": 1,
            "name": "footT",
            "keypoints": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
            "skeleton": []
        }]
    }

    image_id_counter_train = 0  # 用于训练集图片ID计数
    image_id_counter_val = 0    # 用于验证集图片ID计数
    annotation_id_counter = 0

    # 遍历 LabelBee JSON 文件
    for idx, filename in enumerate(os.listdir(labelbee_dir)):
        if filename.endswith(".json"):
            labelbee_json_path = os.path.join(labelbee_dir, filename)
            # 假设图片文件名与 JSON 文件名相同，只是扩展名不同
            image_filename = os.path.splitext(filename)[0]
            image_path = os.path.join(labelbee_dir, image_filename)

            # 检查图片文件是否存在
            if not os.path.exists(image_path):
                print(f"警告：图片 {image_filename} 不存在，跳过该文件...")
                continue

            # 读取图片获取宽高
            try:
                with Image.open(image_path) as img:
                    image_width, image_height = img.size
            except Exception as e:
                print(f"打开图片 {image_path} 时出错: {e}")
                continue

            # 转换为 COCO 格式
            coco_single = convert_to_coco(labelbee_json_path, image_id_counter_train
                                          if idx >= len(os.listdir(labelbee_dir)) * val_ratio
                                          else image_id_counter_val, image_width, image_height)

            if coco_single is None:
                print(f"文件 {filename} 转换时出错，跳过...")
                continue

            # 根据数据集分割，将数据添加到对应的 COCO 数据结构中
            if idx < len(os.listdir(labelbee_dir)) * val_ratio:  # 根据验证集比例决定是训练集还是验证集
                coco_val["images"].append(coco_single["images"][0])
                coco_val["annotations"].extend(coco_single["annotations"])
                shutil.copy(image_path, val_dir)  # 复制图片到验证集文件夹
                image_id_counter_val += 1  # 更新验证集图片ID计数器
            else:
                coco_train["images"].append(coco_single["images"][0])
                coco_train["annotations"].extend(coco_single["annotations"])
                shutil.copy(image_path, train_dir)  # 复制图片到训练集文件夹
                image_id_counter_train += 1  # 更新训练集图片ID计数器

            annotation_id_counter += len(coco_single["annotations"])

    # 写入 COCO JSON 文件
    with open(os.path.join(annotations_dir, 'instances_train.json'), 'w') as f:
        json.dump(coco_train, f, indent=4)

    with open(os.path.join(annotations_dir, 'instances_val.json'), 'w') as f:
        json.dump(coco_val, f, indent=4)

    # 打印检查结果
    train_count = len(coco_train["images"])
    val_count = len(coco_val["images"])
    print(f"总图片数: {train_count + val_count}, 训练集: {train_count}, 验证集: {val_count}")
    print(f"训练集标注总数: {len(coco_train['annotations'])}")
    print(f"验证集标注总数: {len(coco_val['annotations'])}")


# 示例用法
labelbee_dir = "/Users/circle/Desktop/Project/Dataset/footdot_data/labelbee"  # 指定 LabelBee JSON 文件所在的目录
output_dir = "/Users/circle/Desktop/Project/Dataset/footdot_data/coco_600_test"
convert_labelbee_to_paddle(labelbee_dir, output_dir)