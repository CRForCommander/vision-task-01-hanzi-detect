"""
图片读取写入模块

用于读取图片和写入图片

Author: CRForCommander
Date: 2026/11/19
Version: 1.0.0
"""
import cv2
import numpy as np


def readImage(imagePath):
    """
    读取图片

    Args:
        imagePath: 读取图片路径（使用pathlib的Path）

    Returns:
        image: OpenCV能处理的图片矩阵
    """
    # opencv不支持中文，而项目路径含有中文，故不能用 image = cv2.imread(str(imagePath)
    # 把图片读成二进制数据，再解码为OpenCV能处理的图片矩阵
    image = cv2.imdecode(np.fromfile(str(imagePath), dtype=np.uint8), cv2.IMREAD_COLOR)

    # 检查读取结果
    if image is None:
        raise FileNotFoundError(
            "图片读取失败，请检查：\n"
            "1. input 文件夹中是否存在 characters.png\n"
            "2. 文件名和扩展名是否正确\n"
            "3. 图片是否与 main.py 属于同一个项目"
        )

    return image

def saveImage(outputPath,image):
    """
        保存图片到本地

        Args:
            outputPath: 输出图片路径（使用pathlib的Path）
            image: OpenCV能处理的图片矩阵
        """
    #同上，由于不支持中文，故不能用 saved = cv2.imwrite(str(outputPath), image)
    success, buffer = cv2.imencode('.png', image)  # 用imencode把图片数据在内存中编码为png格式的二进制数据buffer

    if success:  # success表示是否编码成功
        buffer.tofile(str(outputPath))  # 再用Python原生的tofile来把编码好的二进制数据写入指定路径，从而避开中文限制
    else:
        raise OSError(f"图片保存失败：{outputPath}")