"""
配置文件模块

用于设置一些常用量

Author: CRForCommander
Date: 2026/11/21
Version: 1.0.0
"""
from pathlib import Path


#项目目录
PROJECT_DIR = Path(__file__).resolve().parent

#输入、输出、模板、编号对应表路径
INPUT_IMAGE_DIR = PROJECT_DIR / "input" / "characters.png"
OUTPUT_DIR = PROJECT_DIR / "output"
TEMPLATE_DIR = PROJECT_DIR / "templates"
MAPPING_PATH = PROJECT_DIR / "mapping.csv"

#红色范围（红色在HSV色环中跨越两端，故需要两个范围）
RED_LOWER_1 = (0, 80, 50)
RED_UPPER_1 = (10, 255, 255)

RED_LOWER_2 = (170, 80, 50)
RED_UPPER_2 = (180, 255, 255)

#蓝色范围
BLUE_LOWER = (100, 60, 40)
BLUE_UPPER = (140, 255, 255)