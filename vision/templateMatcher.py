"""
字符模板匹配模块

用字符模板在原图用交并比来匹配

Author: CRForCommander
Date: 2026/11/23
Version: 1.0.0
"""
import numpy as np

from vision.characterProcessor import createCharacterTemplate


def calculateIou(firstTemplate, secondTemplate):
    """
    计算两张二值字符模板的交并比

    :param firstTemplate: 第一个二值字符模板
    :param secondTemplate: 第二个二值字符模板
    :return: 交并比
    """
    firstBinary = firstTemplate > 0
    secondBinary = secondTemplate > 0

    # 求交
    intersection = np.logical_and(
        firstBinary,
        secondBinary
    )

    # 求并
    union = np.logical_or(
        firstBinary,
        secondBinary
    )

    # 交集数量与并集数量。np.count_nonzero获取非0像素数
    intersectionCount = np.count_nonzero(intersection)
    unionCount = np.count_nonzero(union)

    if unionCount == 0:
        return 0.0

    return intersectionCount / unionCount


def matchCharacter(
    queryTemplate,
    referenceTemplates,
    templatePrefix
):
    """
    将输入字符与指定颜色前缀的参考模板进行比较。

    :param queryTemplate: 需要被查询匹配的模板（原图字符）
    :param referenceTemplates: 用来匹配的模板（字符模板）
    :param templatePrefix: 模板前缀
    :return: bestId：最相似的模板编号； bestScore：最高相似度
    """
    bestId = None       # 最匹配的模板id
    bestScore = -1.0    # 匹配程度

    # 遍历所有参考模板
    for templateId, referenceTemplate in referenceTemplates.items():
        # 红色字符只与 R 模板比较，蓝色字符只与 B 模板比较
        if not templateId.startswith(templatePrefix):
            continue

        # 用交并比计算匹配度
        score = calculateIou(
            queryTemplate,
            referenceTemplate
        )

        # 最终只保留最匹配的
        if score > bestScore:
            bestId = templateId
            bestScore = score

    if bestId is None:
        raise ValueError(
            f"没有找到前缀为 {templatePrefix} 的参考模板。"
        )

    return bestId, bestScore


def recognizeCells(
    image,
    cells,
    referenceTemplates,
    templatePrefix
):
    """
    识别一组格子中的字符，并记录识别结果

    :param image: 原图
    :param cells: 格子列表
    :param referenceTemplates: 字符模板列表
    :param templatePrefix: 模板前缀（R 或 B）
    :return: 识别结果
    """
    # 储存识别结果
    recognitionResults = []

    #逐格子遍历比较
    for cell in cells:
        # 原图建立查询模板
        queryTemplate = createCharacterTemplate(
            image,
            cell
        )

        # 将查询模板进行匹配
        recognizedId, matchScore = matchCharacter(
            queryTemplate,
            referenceTemplates,
            templatePrefix
        )

        # 储存匹配结果
        result = cell.copy()
        result["recognizedId"] = recognizedId
        result["matchScore"] = matchScore

        # 当前的位置编号仅用于检查识别是否正确
        result["isCorrect"] = (
            recognizedId == cell["id"]
        )

        recognitionResults.append(result)

    return recognitionResults