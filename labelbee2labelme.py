import json

def labelbee_keypoints_to_labelme(labelbee_data):
    labelme_data = {
        "version": "4.5.7",
        "flags": {},
        "shapes": [],
        "imagePath": "image.jpg",  # 替换为实际的图像路径
        "imageData": None,
        "imageHeight": labelbee_data["height"],
        "imageWidth": labelbee_data["width"]
    }
    
    for keypoint in labelbee_data["step_1"]["result"]:
        shape_info = {
            "label": "",  # 根据需要添加标签
            "points": [[keypoint["x"], keypoint["y"]]],
            "group_id": None,
            "shape_type": "point",
            "flags": {}
        }
        labelme_data["shapes"].append(shape_info)
    
    return labelme_data

# 从本地文件加载 LabelBee JSON 数据
file_path = "/Users/circle/Desktop/Project/Dataset/footdot_data/result/0_0.jpg.json"  # 替换为实际的文件路径
with open(file_path, "r") as f:
    labelbee_json = f.read()

labelbee_data = json.loads(labelbee_json)

# 将 LabelBee 数据转换为 LabelMe 格式
labelme_data = labelbee_keypoints_to_labelme(labelbee_data)

# 指定输出文件路径
output_file = "output_labelme.json"

# 将 LabelMe 格式数据保存到指定文件
with open(output_file, "w") as f:
    json.dump(labelme_data, f, indent=4)

print(f"转换完成。LabelMe 格式数据已保存到 '{output_file}'。")
