## Labelbee_2_anything
- 此项目下的脚本是为了labelbee格式的json文件转换为paddlepaddle支持的格式方便自定义训练集
  1. labelbee2seg.py为了自定义数据集，实现 ***labelbee*** 的 ***json文件*** 转换伪色彩标注图。
  2. labelbee2labelme.py实现labelbee的json格式转换为labeme的json格式
  3. labelbee2coco.py实现 ***labelbee*** 的json格式转换为 ***coco*** 的json格式

## 地址
[⚡️ *Labelme2seg 代码*](https://github.com/PaddlePaddle/PaddleSeg/blob/release/2.9/tools/data/labelme2seg.py)

## labelbee2seg步骤
- 在`shape2mask`函数中，原来的代码使用`shape['points']`来获取标注形状的点列表。
- 而在修改中，使用了`shape['pointList']`。这个改变意味着修改了标注数据的结构或者是使用了不同的标注工具(labelbee)来生成标注文件。
- 通过这个修改，确保了函数能够正确地从新的标注数据中提取出点列表，并生成对应的掩码图像。
- 在 main 函数中，原来的代码通过遍历每个标注文件的`data['shapes']`来获取形状信息，然后生成标签图像。而修改中，通过遍历每个标注文件的`data`中以 `step_`开头的键对应的值，然后再遍历每个结果中的形状信息来获取标注信息。
- 这个改变可能是因为修改了标注文件的格式或者是添加了新的标注步骤。通过这个修改，确保了代码能够正确地处理新的标注文件结构，并从中提取出正确的形状信息。

## labelbee2coco步骤
2. **convert_to_coco函数：** 这个函数将LabelBee的JSON格式转换为COCO格式。它首先打开指定的LabelBee JSON文件，然后初始化一些变量，包括标注ID计数器和图像ID。然后，它遍历JSON数据中的每个关键点，并将关键点的坐标和其他信息存储在字典中。接着，将字典添加到注释列表中，并返回包含注释和图像信息的字典。

2. **convert_labelbee_to_paddle函数：** 这个函数将LabelBee数据集转换为PaddlePaddle的格式。它首先创建必要的文件夹，包括训练集、验证集和注释目录。然后，初始化了用于存储训练集和验证集信息的字典。接着，它遍历LabelBee JSON文件夹中的每个文件，并读取每个图像的宽度和高度。然后，调用convert_to_coco函数将LabelBee JSON转换为COCO格式，并将结果添加到相应的字典中。最后，将转换后的数据写入到对应的JSON文件中。

4. **示例用法：** 指定LabelBee JSON文件所在的目录和输出目录，并调用convert_labelbee_to_paddle函数进行转换。