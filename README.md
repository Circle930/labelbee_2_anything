## Labelbee_2_anything
- 此项目下的脚本是为了labelbee格式的json文件转换为paddlepaddle支持的格式方便自定义训练集
  1. labelbee2seg.py为了自定义数据集，实现 ***labelbee*** 的 ***json文件*** 转换伪色彩标注图。
  2. labelbee2labelme.py实现labelbee的json格式转换为labeme的json格式

## 地址
[⚡️ *Labelme2seg 代码*](https://github.com/PaddlePaddle/PaddleSeg/blob/release/2.9/tools/data/labelme2seg.py)

## 步骤
- 在`shape2mask`函数中，原来的代码使用`shape['points']`来获取标注形状的点列表。
- 而在修改中，使用了`shape['pointList']`。这个改变意味着修改了标注数据的结构或者是使用了不同的标注工具(labelbee)来生成标注文件。
- 通过这个修改，确保了函数能够正确地从新的标注数据中提取出点列表，并生成对应的掩码图像。
- 在 main 函数中，原来的代码通过遍历每个标注文件的`data['shapes']`来获取形状信息，然后生成标签图像。而修改中，通过遍历每个标注文件的`data`中以 `step_`开头的键对应的值，然后再遍历每个结果中的形状信息来获取标注信息。
- 这个改变可能是因为修改了标注文件的格式或者是添加了新的标注步骤。通过这个修改，确保了代码能够正确地处理新的标注文件结构，并从中提取出正确的形状信息。
