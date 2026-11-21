import csv
from pathlib import Path


def saveMapping(redCells, blueCells, mappingPath):
    """
    将红色和蓝色格子的编号信息保存为 CSV 文件。

    :param red_cells:   红色格子信息
    :param blue_cells:  蓝色格子信息
    :param mapping_path:    保存路径
    """
    mappingPath = Path(mappingPath)
    mappingPath.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "id",
        "color",
        "row",
        "column",
        "x",
        "y",
        "w",
        "h",
        "centerX",
        "centerY",
    ]

    with mappingPath.open(
        mode="w",
        newline="",
        encoding="utf-8-sig"        #让Excel打开CSV时更不容易出现中文乱码
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for cell in redCells + blueCells:
            row = {
                field: cell[field]
                for field in fieldnames
            }
            writer.writerow(row)