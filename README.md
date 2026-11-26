# 基于 OpenCV 的彩色汉字编号识别

## 项目功能

本项目用于识别试题图片中红色、蓝色区域内的 30 个字符，并在原图上显示对应的识别编号。

程序首先使用 HSV 颜色空间分离红色和蓝色区域，通过形态学处理和轮廓检测定位字符格子；随后按照从上到下、每行从左到右的顺序排列格子，并提取字符的白色轮廓。字符经过裁剪和归一化后，被处理为 64×64 像素的二值模板。最后，程序使用模板匹配和交并比（IoU）计算字符相似度，输出相似度最高的模板编号。

## 编号规则

- 红色区域使用 R01～R15；
- 蓝色区域使用 B01～B15；
- 每种颜色均按照三行五列排列；
- 编号顺序为从上到下、每行从左到右；
- 具体编号、颜色及位置对应关系保存在 mapping.csv 中。

## 运行环境

- Python 3.11
- opencv-python
- numpy

安装依赖：

```bash
python -m pip install -r requirements.txt
```

## 使用方法

将试题原图放置在以下位置：

```text
input/characters.png
```

在项目根目录运行：

```bash
python main.py
```

程序会自动完成颜色分离、格子检测、字符模板生成、模板匹配和编号显示，并在控制台输出每个字符的识别编号、相似度及总体识别结果。

## 输出文件

程序运行后主要生成以下文件：

- mapping.csv：字符编号、颜色、行列及坐标对应表；
- templates/：30 张标准化字符模板；
- output/recognitionResult.png：显示识别编号的最终结果图；
- output/templateOverview.png：全部字符模板的总览图。

结果图中的绿色框表示识别编号与预期编号一致，红色框表示识别结果存在差异。

## 项目结构

```text
vision_task1/
├── main.py
├── config.py
├── requirements.txt
├── mapping.csv
├── input/
│   └── characters.png
├── templates/
├── output/
└── vision/
    ├── image_io.py
    ├── color_segmentation.py
    ├── cell_detector.py
    ├── cell_sorter.py
    ├── character_processor.py
    ├── template_matcher.py
    ├── mapping_io.py
    └── visualizer.py
```

## 实现说明

本项目针对题目给定的固定图片设计，使用 OpenCV 完成识别，不需要训练 YOLO 模型。字符模板中的白色表示用于计算的字符轮廓特征，黑色表示背景，不代表字符在原图中的实际颜色。