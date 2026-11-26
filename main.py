"""
主程序

识别图片不同颜色中的不同繁体汉字，并且能够在屏幕上显示出汉字的编号

Author: CRForCommander
Date: 2026/11/19
Version: 1.0.0
"""
import cv2

from config import (
    INPUT_IMAGE_DIR,
    OUTPUT_DIR,
    MAPPING_PATH,
    TEMPLATE_DIR
)
from vision.templateMatcher import recognizeCells
from vision.cellDetector import (
    cleanMask,
    detectCells
)
from vision.cellSorter import sortAndLabelCells
from vision.characterProcessor import createCharacterTemplates
from vision.colorSegmentation import (
    createColorMasks,
    extractColorRegion
)
from vision.imageIO import (
    readImage,
    saveImage
)
from vision.mappingIO import saveMapping
from vision.visualizer import (
    createTemplateOverview,
    drawCell,
    drawRecognitionResults,
)

def printCells(color, cells):
    """
    打印检测到的对应颜色的格子信息

    :param color: 格子颜色
    :param cells: 格子列表
    """
    print(f"\n{color}格子数量： {len(cells)}")

    for index, cell in enumerate(cells, start=1):
        print(
            f"{cell['id']}:"
            f"第{cell['column']}行，{cell['row']}列，"
            f"x={cell['x']}, y={cell['y']}，"
            f"w={cell['w']}, h={cell['h']}"
        )

def main():
    # 读取图片
    image = readImage(INPUT_IMAGE_DIR)
    print("read successfully. Scale: ",image.shape)

    # 创建红蓝掩膜
    redMask, blueMask = createColorMasks(image)

    # 提取原图中红蓝颜色区域
    redRegion = extractColorRegion(image, redMask)
    blueRegion = extractColorRegion(image, blueMask)

    # 保存干净掩膜图片
    saveImage(OUTPUT_DIR / "red_region.png", redRegion)
    saveImage(OUTPUT_DIR / "blue_region.png", blueRegion)

    # 清理掩膜
    cleanedRedMask = cleanMask(redMask)
    cleanedBlueMask = cleanMask(blueMask)

    # 保存干净掩膜图片
    saveImage(OUTPUT_DIR / "cleaned_red_mask.png", cleanedRedMask)
    saveImage(OUTPUT_DIR / "cleaned_blue_mask.png", cleanedBlueMask)

    # 检测格子
    redCells = detectCells(cleanedRedMask)
    blueCells = detectCells(cleanedBlueMask)

    # 将检测到的格子排序并分配正式编号
    redCells = sortAndLabelCells(redCells, "R", "red")
    blueCells = sortAndLabelCells(blueCells, "B", "blue")

    # 绘制格子排序编号结果
    labeledImage = drawCell(image, redCells, color=(0, 255, 0))
    labeledImage = drawCell(labeledImage, blueCells, color=(255, 255, 0))

    # 输出格子信息
    printCells("红色", redCells)
    printCells("蓝色", blueCells)

    # 保存编号对应表
    saveMapping(redCells, blueCells, MAPPING_PATH)

    # 保存编号图
    saveImage(OUTPUT_DIR / "labeled_image.png", labeledImage)

    # 生成字符模板
    redTemplates = createCharacterTemplates(
        image,
        redCells
    )

    blueTemplates = createCharacterTemplates(
        image,
        blueCells
    )

    # 把两个字符模板字典合并为一个字典
    templates = redTemplates | blueTemplates

    # 保存30张独立字符模板
    for cellId, template in templates.items():
        templatePath = TEMPLATE_DIR / f"{cellId}.png"
        saveImage(templatePath, template)

    # 使用模板匹配识别字符
    redResults = recognizeCells(
        image,
        redCells,
        templates,
        templatePrefix="R"
    )

    blueResults = recognizeCells(
        image,
        blueCells,
        templates,
        templatePrefix="B"
    )

    recognitionResults = redResults + blueResults

    # 打印识别结果
    print("\n识别结果：")

    for result in recognitionResults:
        expectedId = result["id"]
        recognizedId = result["recognizedId"]
        matchScore = result["matchScore"]

        print(
            f"位置编号 {expectedId} → "
            f"识别编号 {recognizedId}，"
            f"相似度 {matchScore:.4f}"
        )

    correctCount = sum(
        result["isCorrect"]
        for result in recognitionResults
    )

    print(
        f"\n识别正确数量："
        f"{correctCount}/{len(recognitionResults)}"
    )

    # 绘制并保存识别结果
    recognitionImage = drawRecognitionResults(
        image,
        recognitionResults
    )

    saveImage(
        OUTPUT_DIR / "recognitionResult.png",
        recognitionImage
    )

    # 生成并保存模板总览图
    templateOverview = createTemplateOverview(templates)

    saveImage(OUTPUT_DIR / "templateOverview.png", templateOverview)

    print("识别结果图：", OUTPUT_DIR / "recognitionResult.png")
    print("模板总览图：", OUTPUT_DIR / "templateOverview.png")

    # 显示结果
    cv2.imshow(
        "Recognition Result",
        recognitionImage
    )
    cv2.imshow(
        "Character Templates",
        templateOverview
    )
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()