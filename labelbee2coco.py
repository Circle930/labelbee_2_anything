import json
import os
import shutil
from PIL import Image  # 用于读取图片尺寸




def convert_to_coco(labelbee_json_path, image_id, image_width, image_height):
    with open(labelbee_json_path, 'r') as f:
        labelbee_data = json.load(f)

    coco_annotations = []

    for point_data in labelbee_data["step_1"]["result"]:
        annotation_info = {
            "num_keypoints": 1,  # 假设每个点只有一个关键点
            "area": image_width * image_height,  # 整个图像的面积
            "iscrowd": 0,  # 假设每个点都不是群集
            "keypoints": [int(point_data["x"]), int(point_data["y"]), 2], 
            "image_id": image_id,  # 图像ID
            "bbox": [0, 0, image_width, image_height],  # 整个图像作为边界框
            "category_id": 1,  # 假设所有点都属于同一类别
            "id": len(coco_annotations) + 1,  # 每个标注的唯一ID
        }
        coco_annotations.append(annotation_info)

    return {
        "annotations": coco_annotations,
        "images": [{
            "file_name": os.path.splitext(os.path.basename(labelbee_json_path))[0] + ".jpg",
            "height": image_height,
            "width": image_width,
            "id": image_id
        }]
    }




def convert_labelbee_to_paddle(labelbee_dir, output_dir):
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
        "categories": [{"id": 1, "name": "category_name", "supercategory": "supercategory_name"}]  # 填入实际类别信息
    }
    coco_val = {
        "images": [],
        "annotations": [],
        "categories": [{"id": 1, "name": "category_name", "supercategory": "supercategory_name"}]  # 填入实际类别信息
    }

    image_id_counter = 0
    annotation_id_counter = 0

    # 遍历 LabelBee JSON 文件
    for filename in os.listdir(labelbee_dir):
        if filename.endswith(".json"):
            labelbee_json_path = os.path.join(labelbee_dir, filename)
            # 假设图片文件名与 JSON 文件名相同，只是扩展名不同
            image_filename = os.path.splitext(filename)[0]
            image_path = os.path.join(labelbee_dir, image_filename)

            # 读取图片获取宽高
            with Image.open(image_path) as img:
                image_width, image_height = img.size

            # 转换为 COCO 格式
            coco_single = convert_to_coco(labelbee_json_path, image_id_counter, image_width, image_height)

            # 根据数据集分割，将数据添加到对应的 COCO 数据结构中
            if ...:  # 判断条件，根据分割结果决定是训练集还是验证集
                coco_train["images"].append(coco_single["images"][0])
                coco_train["annotations"].extend(coco_single["annotations"])
                shutil.copy(image_path, train_dir)  # 复制图片到训练集文件夹
            else:
                coco_val["images"].append(coco_single["images"][0])
                coco_val["annotations"].extend(coco_single["annotations"])
                shutil.copy(image_path, val_dir)  # 复制图片到验证集文件夹

            image_id_counter += 1
            annotation_id_counter += len(coco_single["annotations"])

    # 写入 COCO JSON 文件
    with open(os.path.join(annotations_dir, 'instance_train.json'), 'w') as f:
        json.dump(coco_train, f, indent=4)

    with open(os.path.join(annotations_dir, 'instance_val.json'), 'w') as f:
        json.dump(coco_val, f, indent=4)




# 示例用法
labelbee_dir = "labelbee"  # 指定 LabelBee JSON 文件所在的目录
output_dir = "paddle_format"  
convert_labelbee_to_paddle(labelbee_dir, output_dir)