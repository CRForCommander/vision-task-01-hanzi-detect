"""
可视化模块

展示图片字符标注效果

Author: CRForCommander
Date: 2026/11/21
Version: 1.0.0
"""
import cv2
import numpy as np


def drawCell(image, cells, color):
    """
    在图片上绘制格子矩形和格子编号

    :param image: 待绘制图片
    :param cells: 格子列表
    :param color: BGR颜色
    :return: 绘制过的图片
    """
    # 复制一份，不破坏原图
    output = image.copy()

    for index, cell in enumerate(cells, start=1):   #enumerate()用于对于要遍历的东西同时拿到元素和序号
        x = cell["x"]
        y = cell["y"]
        w = cell["w"]
        h = cell["h"]

        #有正式编号就使用正式编号，否则使用临时编号
        label = cell.get("id", str(index))

        #绘制格子矩形框
        cv2.rectangle(
            output,         #要绘制的图片
            (x, y),         #对角顶点1
            (x + w, y + h), #对角顶点2
            color,          #矩形颜色
            2               #线条颜色（使用BGR而不是RGB）
        )
        #按顺序绘制对应临时编号
        cv2.putText(
            output,                                 #要绘制的图片
            text=label,                             #要绘制的文字
            org=(x + 3, max(y + 20, 20)),           #文字的左下角坐标
            fontFace = cv2.FONT_HERSHEY_SIMPLEX,    #字体类型。cv2.FONT_HERSHEY_SIMPLEX：无衬线常规字体
            fontScale=0.6,                          #字体缩放倍数。1.0为标准大小
            color=color,                            #文字颜色（使用BGR而不是RGB）
            thickness=2                             #文字笔画粗细（像素）
        )

    return output

def createTemplateOverview(templates):
    """
    将30张字符模板排列成一张总览图


    :param templates: 模板列表
    :return: 总览图
    """
    tileSize = 100      # 每个模板要画的边长
    columns = 5         # 列数
    templateSize = 64   # 模板图片大小

    templateItems = list(templates.items())                 # 字符模板配id的列表
    rows = (len(templateItems) + columns - 1) // columns    # 行数

    # 创建白色底图
    overview = np.full(
        (rows * tileSize, columns * tileSize, 3),   # 宽度，高度，3个通道
        255,    # 白色
        dtype=np.uint8
    )

    for index, (cellId, template) in enumerate(templateItems):
        row = index // columns      # 第几行
        column = index % columns    # 第几列

        # 字符模板要画的格子的左上角起点
        startX = column * tileSize
        startY = row * tileSize

        # 图片灰度转BGR格式
        templateBgr = cv2.cvtColor(
            template,
            cv2.COLOR_GRAY2BGR
        )

        # 字符模板要画的居中位置的左上角起点
        offsetX = startX + (tileSize - templateSize) // 2
        offsetY = startY + 24

        # 将字符模板贴到白色背景对应位置
        overview[
            offsetY:offsetY + templateSize,
            offsetX:offsetX + templateSize
        ] = templateBgr

        # 画上对应编号
        cv2.putText(
            overview,
            cellId,
            (startX + 31, startY + 18),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 0),
            1
        )

        # 绘制字符模板格子边框
        cv2.rectangle(
            overview,
            (startX, startY),
            (startX + tileSize - 1, startY + tileSize - 1),
            (180, 180, 180),
            1
        )

    return overview

def drawRecognitionResults(image, recognitionResults):
    """
    绘制识别结果。

    :param image: 原图
    :param recognitionResults: 识别结果
    :return: 识别结果图片。绿色：识别编号与位置编号一致；红色：识别编号与位置编号不一致
    """
    output = image.copy()

    for result in recognitionResults:
        x = result["x"]
        y = result["y"]
        width = result["w"]
        height = result["h"]

        recognizedId = result["recognizedId"]
        isCorrect = result["isCorrect"]

        # 不正确红色，正确则绿色
        color = (
            (0, 255, 0)
            if isCorrect
            else (0, 0, 255)
        )

        # 绘制边框
        cv2.rectangle(
            output,
            (x, y),
            (x + width, y + height),
            color,
            2
        )

        # 添加识别结果文字
        cv2.putText(
            output,
            recognizedId,
            (x + 3, max(y + 22, 22)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            color,
            2
        )

    return output
