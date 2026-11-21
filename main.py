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
    MAPPING_PATH
)
from vision.cellDetector import (
    cleanMask,
    detectCells
)
from vision.cellSorter import sortAndLabelCells
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
    drawCell
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

    # 显示图片
    cv2.imshow("Labeled Cells", labeledImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()