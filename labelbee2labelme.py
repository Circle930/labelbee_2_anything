import json
import os

def labelbee_keypoints_to_labelme(labelbee_data, image_file):
    labelme_data = {
        "version": "4.5.7",
        "flags": {},
        "shapes": [],
        "imagePath": os.path.basename(image_file),  
        "imageData": None,
        "imageHeight": labelbee_data["height"],
        "imageWidth": labelbee_data["width"]
    }
    
    for keypoint in labelbee_data["step_1"]["result"]:
        shape_info = {
            "label": "",  
            "points": [[keypoint["x"], keypoint["y"]]],
            "group_id": None,
            "shape_type": "point",
            "flags": {}
        }
        labelme_data["shapes"].append(shape_info)
    
    return labelme_data

def batch_labelbee_to_labelme(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            input_file = os.path.join(input_dir, filename)
            output_file = os.path.splitext(os.path.basename(filename))[0]  # 删除扩展名
            with open(input_file, "r") as f:
                labelbee_data = json.load(f)
            labelme_data = labelbee_keypoints_to_labelme(labelbee_data, input_file)
            output_file = filename.replace(".jpg", "")
            output_file = os.path.join(output_dir, output_file)  # 添加后缀
            
            with open(output_file, "w") as f:
                json.dump(labelme_data, f, indent=4)
            print(f"转换完成。LabelMe 格式数据已保存到 '{output_file}'。")

# 指定输入目录和输出目录
input_dir = "/Users/circle/Desktop/Project/Dataset/footdot_data/test/"  # 替换为实际的输入目录
output_dir = "/Users/circle/Desktop/Project/Dataset/footdot_data/labelme/"  # 替换为实际的输出目录

# 批量转换
batch_labelbee_to_labelme(input_dir, output_dir)
