from kivy.config import Config
import kivy.app
from kivy.properties import ObjectProperty, ListProperty, StringProperty
from kivy.graphics import Color, Line
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.animation import Animation

import utils
from utils import kivy_utils
from utils.page_utils import Page, Bubble
from . import app_events

Config.set('kivy', 'log_level', 'debug')


class App(kivy.app.App):
	viewer= ObjectProperty(None)
	tl_table= ObjectProperty(None)
	vocab_panel= ObjectProperty(None)

	def __init__(self, glob_dir, chap_num, series="knight", mtl=False):
		super().__init__()
		self.glob_dir= glob_dir
		self.chap_num= chap_num
		self.series= series

		self.mtl= mtl


	def build(self):
		self.root= Builder.load_file(utils.KIVY_CLASS_DIR + "app.kv")

		self.title= "Translation Thingy"
		self.pages= Page.load_pages(series=self.series, chap_num=self.chap_num, glob_dir=self.glob_dir)

		print("populating viewer")
		self.populate_viewer()
		print("populating table")
		self.populate_table(mtl=self.mtl)
		print("populating vocab")
		self.populate_vocab()

		self.populate_events()

		return self.root

	def populate_table(self, mtl=False):
		# table
		self.tl_table= self.root.ids.tl_table.build()

		# table data
		self.tl_table.populate_from_pages(self.pages, mtl=mtl)

	def populate_vocab(self):
		self.vocab_panel= self.root.ids.vocab_panel.build()
		self.vocab_panel.pinTab.add_words([
				# todo: placeholder
				{ "name": "aaa" },
				{ "name": "ccc" },
				{ "name": "bbb" },
				{ "name": "eee" },
				{ "name": "ddd" }
			])

	def populate_viewer(self):
		self.viewer= self.root.ids.viewer.build(self.pages, hidden=True)

	def populate_events(self):
		self.tl_table.on_focus.append(app_events.highlight_on_focus)
		self.tl_table.on_double_click.append(app_events.scroll_on_table_double_click)
		self.viewer.on_double_click.append(app_events.scroll_on_bubble_double_click)

		self.tbl_buttons= self.root.ids.tbl_buttons.build()
		return self