import argparse
import glob
import os
import os.path as osp
import shutil
import json
import numpy as np
import PIL.Image
import PIL.ImageDraw

def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('input_dir', help='input annotated directory')
    parser.add_argument('output_dir', help='output annotated directory')
    return parser.parse_args()

def get_color_map_list(num_classes):
    num_classes += 1
    color_map = num_classes * [0, 0, 0]
    for i in range(0, num_classes):
        j = 0
        lab = i
        while lab:
            color_map[i * 3] |= (((lab >> 0) & 1) << (7 - j))
            color_map[i * 3 + 1] |= (((lab >> 1) & 1) << (7 - j))
            color_map[i * 3 + 2] |= (((lab >> 2) & 1) << (7 - j))
            j += 1
            lab >>= 3
    color_map = color_map[3:]
    return color_map

def shape2mask(img_size, shape):
    label_mask = PIL.Image.fromarray(np.zeros(img_size[:2], dtype=np.uint8))
    image_draw = PIL.ImageDraw.Draw(label_mask)
    points = shape['pointList']
    polygon = [(point['x'], point['y']) for point in points]
    image_draw.polygon(polygon, outline=1, fill=1)
    return np.array(label_mask, dtype=bool)

def main(args):
    # prepare
    output_dir = args.output_dir
    output_img_dir = osp.join(args.output_dir, 'images')
    output_annot_dir = osp.join(args.output_dir, 'annotations')
    if not osp.exists(output_dir):
        os.makedirs(output_dir)
        print('Creating directory:', output_dir)
    if not osp.exists(output_img_dir):
        os.makedirs(output_img_dir)
        print('Creating directory:', output_img_dir)
    if not osp.exists(output_annot_dir):
        os.makedirs(output_annot_dir)
        print('Creating directory:', output_annot_dir)

    # collect and save class names
    class_names = ['_background_']
    for label_file in glob.glob(osp.join(args.input_dir, '*.json')):
        with open(label_file) as f:
            data = json.load(f)
            for step_key in data:
                if step_key.startswith('step_'):
                    step = data[step_key]
                    for shape in step['result']:
                        cls_name = shape['attribute']
                        if cls_name not in class_names:
                            class_names.append(cls_name)

    class_name_to_id = {}
    for i, class_name in enumerate(class_names):
        class_id = i  # starts with 0
        class_name_to_id[class_name] = class_id
    print('class_names:', class_names)

    out_class_names_file = osp.join(output_dir, 'class_names.txt')
    with open(out_class_names_file, 'w') as f:
        f.writelines('\n'.join(class_names))
    print('Saved class_names:', out_class_names_file)

    # create annotated images and copy origin images
    color_map = get_color_map_list(256)
    for label_file in glob.glob(osp.join(args.input_dir, '*.json')):
        print('Generating dataset from:', label_file)
        filename = osp.splitext(osp.basename(label_file))[0]
        # 去除文件名中的".jpg"
        new_filename = filename.replace(".jpg", "")
        annotated_img_path = osp.join(output_annot_dir, new_filename + '.png')
        with open(label_file) as f:
            data = json.load(f)
            img_path = osp.join(args.input_dir, filename)
            shutil.copy(img_path, output_img_dir)

            lbl = np.zeros((data['height'], data['width']), dtype=np.int32)
            for step_key in data:
                if step_key.startswith('step_'):
                    step = data[step_key]
                    for shape in step['result']:
                        lbl_mask = shape2mask((data['height'], data['width']), shape)
                        lbl[lbl_mask] = class_name_to_id[shape['attribute']]

            lbl_pil = PIL.Image.fromarray(lbl.astype(np.uint8), mode='P')
            lbl_pil.putpalette(color_map)
            lbl_pil.save(annotated_img_path)

if __name__ == '__main__':
    args = parse_args()
    main(args)