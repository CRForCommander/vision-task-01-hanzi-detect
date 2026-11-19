"""
主程序

识别图片不同颜色中的不同繁体汉字，并且能够在屏幕上显示出汉字的编号

Author: CRForCommander
Date: 2026/11/19
Version: 1.0.0
"""
import cv2

from config import INPUT_IMAGE_DIR, OUTPUT_DIR
from vision.colorSegmentation import (
    createColorMasks,
    extractColorRegion,
)
from vision.imageIO import readImage, saveImage


def main():
    #读取图片
    image = readImage(INPUT_IMAGE_DIR)
    print("read successfully. Scale: ",image.shape)

    #创建红蓝掩膜
    redMask, blueMask = createColorMasks(image)

    #提取原图中红蓝颜色区域
    redRegion = extractColorRegion(image, redMask)
    blueRegion = extractColorRegion(image, blueMask)

    #保存结果
    saveImage(OUTPUT_DIR / "red_mask.png",redMask)
    saveImage(OUTPUT_DIR / "blue_mask.png",blueMask)
    saveImage(OUTPUT_DIR / "red_region.png",redRegion)
    saveImage(OUTPUT_DIR / "blue_region.png",blueRegion)

    print("Saved at: ", OUTPUT_DIR)

    #展示掩膜
    cv2.imshow("red mask", redMask)
    cv2.waitKey(0)
    cv2.imshow("blue mask", blueMask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()