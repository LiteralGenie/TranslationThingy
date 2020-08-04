from kivy.config import Config
from kivy.app import App
from kivy.properties import ObjectProperty, DictProperty, StringProperty
from kivy.graphics import Color, Line
from kivy.lang import Builder

import utils, kivy_utils
from utils.ocr_utils import gapi
from utils.korean_utils import Page, Bubble
from scratch.v2.tlt_events import highlight_bubble, remove_box # @TODO: fix temporary import

Config.set('kivy', 'log_level', 'debug')


class TltApp(App):
	viewer= ObjectProperty(None)
	tl_table= ObjectProperty(None)
	vocab_panel= ObjectProperty(None)

	def __init__(self, glob_dir, chap_num):
		super().__init__()
		self.glob_dir= glob_dir
		self.chap_num= chap_num
		self.series= "knight"

		self.pages= []
		self.pages_bubbles_rows= []

	def build(self):
		self.title= "Translation Thingy"
		self.root= Builder.load_file(utils.ROOT_DIR + "scratch/v2/tlt.kv") # TODO: another temp path

		self.populate_viewer()
		self.populate_table()
		self.populate_vocab()

		return self.root

	def populate_table(self):
		# table
		self.tl_table= self.root.ids.tl_table.build()

		# table data
		self.pages= Page.load_pages(series=self.series, chap_num=self.chap_num, glob_dir=self.glob_dir)
		for pg in self.pages:
			for bubb in pg.bubbles:
				r= self.tl_table.append_row(kor=bubb.raw_text, on_focus=highlight_bubble)
				self.pages_bubbles_rows.append({"bubble": bubb, "row": r, "page": pg})

	def populate_vocab(self):
		self.vocab_panel= self.root.ids.vocab_panel.build()
		self.vocab_panel.pinTab.add_words([
				{ "name": "aaa" },
				{ "name": "ccc" },
				{ "name": "bbb" },
				{ "name": "eee" },
				{ "name": "ddd" }
			])

	def populate_viewer(self):
		self.viewer= self.root.ids.viewer.build(globDir=self.glob_dir, chapNum=self.chap_num)

		# higlight box
		with self.viewer.canvas:
			Color(1,0,0,0.3)
			self.bubbBox= Line(size=(110,110), width=1.25, dash_length=0.5, dash_offest=1)

		# remove highlight box on scroll
		self.viewer.fbind('on_scroll_stop', remove_box)

if __name__ == "__main__":
	chapNum= 209
	globDir= rf"C:\scans\Knight Run\{chapNum}/*.png"

	kivy_utils.doFullScreen()
	TltApp(glob_dir=globDir, chap_num=chapNum).run()