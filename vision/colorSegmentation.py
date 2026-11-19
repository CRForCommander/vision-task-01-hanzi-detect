"""
颜色分离模块

根据图片蓝色和红色来生成掩膜

Author: CRForCommander
Date: 2026/11/19
Version: 1.0.0
"""
import cv2

#导入配置参数
from config import (
    BLUE_LOWER,
    BLUE_UPPER,
    RED_LOWER_1,
    RED_UPPER_1,
    RED_LOWER_2,
    RED_UPPER_2,
)

def createColorMasks(image):
    """
    从原图中创建红色、蓝色掩膜

    :param image： 原始图像矩阵数据
    :return: redMask: 红色区域掩膜 | blueMask: 蓝色区域掩膜
    """
    #图片从BGR格式的转为HSV格式的（相比于BGR更适合找某种颜色的范围）
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    #用inRange函数把符合颜色的范围的像素找出来，生成一个黑白掩膜（Mask），对应颜色为白色，其他都是黑色
    redMask1 = cv2.inRange(
        hsv, RED_LOWER_1, RED_UPPER_1
    )
    redMask2 = cv2.inRange(
        hsv, RED_LOWER_2, RED_UPPER_2
    )
    #合并两个红色范围的掩膜得到完整红色掩膜（两张掩膜在某个像素点都为黑色（0）时，结果才为黑色，否则都是白色）
    redMask = cv2.bitwise_or(redMask1, redMask2)

    blueMask = cv2.inRange(
        hsv, BLUE_LOWER, BLUE_UPPER
    )

    return redMask, blueMask

def extractColorRegion(image, mask):
    """
    根据掩膜保留原图中的指定颜色区域

    :param image： 原始图像矩阵数据
    :param mask: 掩膜
    :return: 根据掩膜保留的原图中指定颜色区域
    """
    return cv2.bitwise_and(image, image, mask=mask)