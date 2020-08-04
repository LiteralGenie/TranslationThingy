from .text_input import TxtInput
from .viewer import Viewer
from .translation_table import TranslationTable
from .vocab_tabs import VocabPanel

import utils
from kivy.lang import Builder

# Loads at the module-level to avoid duplicate calls
Builder.load_file(utils.KIVY_CLASS_DIR + "translation_table_layout.kv")
Builder.load_file(utils.KIVY_CLASS_DIR + "vocab_tabs_layout.kv")