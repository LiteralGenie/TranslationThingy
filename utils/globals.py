import pathlib
from utils.misc_utils import loadJson

ROOT_DIR= str(pathlib.Path(__file__).parent.parent) + "/"


DATA_DIR= ROOT_DIR + "data/"
KIVY_UTILS_DIR= ROOT_DIR + "kivy_utils/"
CONFIG_DIR= ROOT_DIR + "config/"


FONT_DIR= DATA_DIR + "/fonts"
ENDIC_DIR= DATA_DIR + "endic/"
OCR_DIR= DATA_DIR + "ocr/"
PAPAGO_CACHE= DATA_DIR + "papago.json"


CONFIG= loadJson(CONFIG_DIR + "config.json")
FONT_PATH_1= DATA_DIR + CONFIG['font_1']


KIVY_CLASS_DIR= KIVY_UTILS_DIR + "classes/"