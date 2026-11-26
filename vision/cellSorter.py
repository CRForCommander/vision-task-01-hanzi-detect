"""
字符格子编号模块

排列格子，并分配正式编号

Author: CRForCommander
Date: 2026/11/20
Version: 1.0.0
"""


def sortAndLabelCells(cells, prefix, color):
    """
    将检测出的15个格子排列成三行五列，并分配正式编号

    :param cells: cellDetector()检测到的格子列表
    :param prefix: 编号前缀，如 R 或 B
    :param color: 颜色名称， 如 red 或 blue
    :return: 带有 id、 row、 column 等信息的格子列表
    """
    if len(cells) != 15:
        raise ValueError(
            f"{color} 区域应检测到15个格子"
            f"实际检测到 {len(cells)} 个，请检查格子检测结果"
        )

    # 先按中心点纵坐标，从上到下排列
    temp = sorted(cells, key=lambda cell: cell["centerY"])

    #存储按照纵坐标初步分行粗排的格子
    rows = []

    #将纵坐标解决的格子归入同一行
    for cell in temp:
        if not rows:    # 如果rows为空，则直接将[cell]添加进去作为新的一行
            rows.append([cell])
            continue
        # 从最后一行作为当前处理行。因为最后一行是新的要排入的行，前面的都是排好的
        currentRow = rows[-1]

        # 求当前处理行的平均字符中心点纵坐标
        averageY = sum(item["centerY"] for item in currentRow) / len(currentRow)
        # 求当前处理行的平均字符高度
        averageH = sum(item["h"] for item in currentRow) / len(currentRow)

        # 求误差。纵坐标相差不到半个格子高度，应视为同一行
        tolerance = max(cell["h"], averageH) * 0.5

        if abs(averageY - cell["centerY"]) <= tolerance:
            currentRow.append(cell)     # 相差不大是同一行
        else:
            rows.append([cell])         #相差过大视为新一行

    # 排好的每行格子数量
    rowSizes = [len(row) for row in rows]

    # 异常情况
    if len(rows) != 3 or any(size != 5 for size in rowSizes):
        raise ValueError(
            f"{color} 区域无法排列成三行五列"
            f"当前总行数为 {len(rows)}，每行格子数为 {rowSizes}"
        )

    # 存储排好且编号的格子
    labeldCells = []

    # 每行内部再按照 centerX 从左到右排列.每行排列了后再进行编号
    for rowIndex, row in enumerate(rows,start=1):
        # 一行按照 centerX 从左到右排列
        sortedRow = sorted(row, key=lambda cell: cell["centerX"])

        for columnIndex, column in enumerate(sortedRow,start=1):
            labeledCell = column.copy()               #复制一份格子的数据，这样不改变原数据

            number = (rowIndex - 1) * 5 + columnIndex   #编号

            #添加数据
            labeledCell["id"] = f"{prefix}{number:02d}"
            labeledCell["color"] = color
            labeledCell["row"] = rowIndex
            labeledCell["column"] = columnIndex

            labeldCells.append(labeledCell)

    return labeldCells
