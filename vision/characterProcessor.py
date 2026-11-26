"""
字符轮廓提取处理模块

根据之前检测出的格子，提取其中的字符白色轮廓并处理

Author: CRForCommander
Date: 2026/11/23
Version: 1.0.0
"""
import cv2
import numpy as np


def extractWhiteMask(cellImage):
    """
    从单个彩色格子中提取字符白色轮廓

    :param cellImage: 单个格子的图片
    :return: 从单个格子中提取的字符白色轮廓
    """
    # 图片转为HSV格式
    cellHsv = cv2.cvtColor(
        cellImage,
        cv2.COLOR_BGR2HSV
    )

    # 白色轮廓：低饱和度、高明度
    whiteMask = cv2.inRange(
        cellHsv,
        (0, 0, 150),
        (180, 90, 255)
    )

    return whiteMask


def cropCharacter(whiteMask):
    """
    裁剪出所有白色轮廓共同占据的矩形范围

    :param whiteMask: 白色轮廓
    :return: <UNK>
    """
    # 提取二值图像所有白色（非0）像素坐标
    whitePoints = cv2.findNonZero(whiteMask)

    if whitePoints.size == 0:
        raise ValueError("没有检测到白色轮廓，请检查白色提取阈值。")

    # 获取白色轮廓的矩形边框。cv2.boundingRect(whitePoints)计算一组点或一个非零区域的正矩形外接框
    x, y, width, height = cv2.boundingRect(whitePoints)

    # 给矩形边框添加少量边距，避免裁掉边缘笔画
    padding = 2
    maskHeight, maskWidth = whiteMask.shape

    startX = max(0, x - padding)
    startY = max(0, y - padding)
    endX = min(maskWidth, x + width + padding)
    endY = min(maskHeight, y + height + padding)

    characterImage = whiteMask[
        startY:endY,
        startX:endX
    ]

    return characterImage


def normalizeCharacter(characterImage, canvasSize=64, padding=4):
    """
    保持字符白色轮廓长宽比，将字符白色轮廓放入统一大小的黑色画布，作为字符模板
    即归一化。防止直接比较原始裁剪图导致即使字符相同，也可能因为大小和位置不同而匹配失败

    :param characterImage: 单个字符白色轮廓图片
    :param canvasSize: 画布大小
    :param padding: 预留边距
    :return: 单个字符模板
    """
    characterHeight, characterWidth = characterImage.shape

    availableSize = canvasSize - 2 * padding

    # 缩放倍率
    scale = min(
        availableSize / characterWidth,
        availableSize / characterHeight
    )

    # 缩放后宽度
    resizedWidth = max(
        1,
        round(characterWidth * scale)
    )
    # 缩放后高度
    resizedHeight = max(
        1,
        round(characterHeight * scale)
    )

    # 使用最近邻插值进行缩放，保持二值图的黑白特性
    resizedCharacter = cv2.resize(
        characterImage,
        (resizedWidth, resizedHeight),
        interpolation=cv2.INTER_NEAREST
    )

    # 创建正方形黑色画布
    canvas = np.zeros(
        (canvasSize, canvasSize),
        dtype=np.uint8  #8位，0~255
    )

    # 计算字符轮廓图左上角应居中贴在画板的哪个位置
    offsetX = (canvasSize - resizedWidth) // 2
    offsetY = (canvasSize - resizedHeight) // 2

    # 把字符轮廓图贴到画布上
    canvas[
        offsetY:offsetY + resizedHeight,
        offsetX:offsetX + resizedWidth
    ] = resizedCharacter

    return canvas


def createCharacterTemplate(image, cell):
    """从原图的一个格子中创建标准字符模板

    :param image: 原图
    :param cell: 一个格子列表，里面是格子的具体信息
    :return: 一个标准字符模板
    """
    x = cell["x"]
    y = cell["y"]
    width = cell["w"]
    height = cell["h"]

    #裁剪下原图对应格子位置
    cellImage = image[
        y:y + height,
        x:x + width
    ]

    whiteMask = extractWhiteMask(cellImage)
    characterImage = cropCharacter(whiteMask)
    template = normalizeCharacter(characterImage)

    return template


def createCharacterTemplates(image, cells):
    """
    为一组格子创建模板。

    :param image: 原图
    :param cells: 格子总列表
    :return: 字典，键为字符编号，值为64×64模板图片
    """
    templates = {}

    for cell in cells:
        cellId = cell["id"]

        try:
            template = createCharacterTemplate(
                image,
                cell
            )
        except ValueError as error:
            raise ValueError(
                f"{cellId} 模板生成失败：{error}"
            ) from error

        templates[cellId] = template

    return templates