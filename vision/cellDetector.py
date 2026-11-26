"""
字符格子检测模块

清理掩膜、查找轮廓、过滤噪点、提取格子

Author: CRForCommander
Date: 2026/11/23
Version: 1.0.0
"""
import cv2
import numpy as np


def cleanMask(mask):
    """
    清理掩膜中的噪点和小缺口

    :param mask: 掩膜
    :return: 清理干净的掩膜
    """
    # 创建开运算和闭运算需要的核
    openKernal = np.ones((3, 3), np.uint8)
    closeKernal = np.ones((5, 5), np.uint8)

    # 开运算，清除较小的白色噪点
    cleaned = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        openKernal
    )
    # 闭运算，连接白色区域的小缺口
    cleaned = cv2.morphologyEx(
        cleaned,
        cv2.MORPH_CLOSE,
        closeKernal
    )

    return cleaned

def detectCells(mask):
    """
    从颜色掩膜中检测字符格子

    :param mask: 掩膜
    :return: 返回一个列表，每个元素是一个字典，保存格子的位置和尺寸
    """
    # 反转掩膜，使字符变黑色，背景变白色，否则直接用会提取一个包含所有字符的超大外框，而不是一个独立字符
    mask =cv2.bitwise_not(mask)

    # 如果是三通道图片，转为单通道。cv2.findContours只支持单通道
    #if len(mask.shape) == 3:
    #    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

    # 扫描图片，寻找所有白色连通区域的轮廓线，得到它们的形状和坐标
    # contours（轮廓列表）：一个包含所有轮廓的列表。每个元素就是一个白色格子的边界点坐标
    # hierarchy（层级关系）：记录轮廓直接谁套着谁的关系。不过由于这里使用cv2.RETR_EXTERNAL(只提取最外层)，所以没用
    contours, hierarchy = cv2.findContours(
        mask,
        cv2.RETR_LIST,          # 提取所有轮廓，大的背景轮廓会在接下来被过滤掉
        cv2.CHAIN_APPROX_SIMPLE     # 压缩直线段，对于一条直线不是记录每个像素点，而是只记录起点和终点，提高运行速度
    )
    # contours包含：
    # 1. 白色背景的轮廓
    # 2. 白色字符的轮廓
    # 3. 噪点的轮廓

    # 获取掩膜图片的长宽并计算面积
    imageHeight, imageWidth = mask.shape[0], mask.shape[1]
    imageArea = imageHeight * imageWidth

    # 由于读取的轮廓可能有大有小，还会有错误读取噪点，所以使用相对尺寸作为阈值过滤，避免完全依赖固定像素值的读取误差过大
    minArea = imageArea * 0.002
    maxArea = imageArea * 0.1
    minWidth = imageWidth * 0.02
    minHeight = imageHeight * 0.02

    cells = []

    #逐个筛查，排除不合格轮廓
    for contour in contours:
        # 获取轮廓的面积用于判断
        area = cv2.contourArea(contour)
        #获取包住轮廓的外接矩形框
        x, y, w, h = cv2.boundingRect(contour)

        # 过滤面积异常的轮廓
        if area < minArea or area > maxArea:
            continue

        # 过滤宽、高过小的轮廓
        if w < minWidth or h < minHeight:
            continue

        # 用字典形式保存合格轮廓的外围方框，并添加进列表
        cell = {
            "x": x,     #起始点x
            "y": y,     #起始点y
            "w": w,     #方框宽
            "h": h,     #方框高
            "area": area,       #轮廓面积
            "centerX": x + w // 2,     #方框中心x
            "centerY": y + h // 2,     #方框中心y
        }
        cells.append(cell)

    return cells


