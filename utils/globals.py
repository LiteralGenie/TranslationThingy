import pathlib

ROOT_DIR= str(pathlib.Path(__file__).parent.parent) + "/"

CONFIG_DIR= ROOT_DIR + "config/"

DATA_DIR= ROOT_DIR + "data/"
ENDIC_DIR= DATA_DIR + "endic/"
OCR_DIR= DATA_DIR + "ocr/"
PAPAGO_CACHE= DATA_DIR + "papago.json"

# GOOGLE_SERVICE_ACCOUNT= "981443074237-compute@developer.gserviceaccount.com"

KIVY_UTILS_DIR= ROOT_DIR + "kivy_utils/"
KIVY_CLASS_DIR= KIVY_UTILS_DIR + "classes/"

FONT_PATH= DATA_DIR + "fonts/NotoSansKR-Regular.otf"