from .txt_input import TxtInput
from .viewer import Viewer
from .translation_table import TranslationTable
from .vocab_tabs import VocabPanel
from .table_buttons import TableButtons

import utils
from kivy.lang import Builder


# Loads at the module-level to avoid duplicate calls
Builder.load_file(utils.KIVY_CLASS_DIR + "translation_table_layout.kv")
Builder.load_file(utils.KIVY_CLASS_DIR + "vocab_tabs_layout.kv")
Builder.load_file(utils.KIVY_CLASS_DIR + "txt_input_layout.kv")
Builder.load_file(utils.KIVY_CLASS_DIR + "viewer_layout.kv")
Builder.load_file(utils.KIVY_CLASS_DIR + "table_buttons_layout.kv")
