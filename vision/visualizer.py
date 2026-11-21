"""
可视化模块

展示图片字符标注效果

Author: CRForCommander
Date: 2026/11/21
Version: 1.0.0
"""
import cv2


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

