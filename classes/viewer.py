from utils import kivy_utils # call builder for below classes
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty, NumericProperty, ListProperty
from .im_page import ImPage

from utils.page_utils import Page
import functools


class Viewer(ScrollView):
	layout = ObjectProperty()
	float_layout = ObjectProperty()
	overlay= ObjectProperty()

	def build(self, pages, hidden=True):
		self.pages= pages
		self.im_pages= []
		self.load_images(hidden=hidden)
		return self

	def load_images(self, hidden=True):
		for pg in self.pages:
			im_pg= ImPage().build(	page=pg,
									im_path=pg.im_path,
									page_index=pg.page_num
		  	)
			self.im_pages.append(im_pg)
			self.layout.add_widget(im_pg)

		self.im_heights= [x.height for x in self.im_pages]
		self.float_layout.height= self.layout.height= sum(self.im_heights)

		w= self.bar_width + max([ x.width for x in self.im_pages ])
		self.width= self.layout.width= self.float_layout.width= w

		# draw bbox for each bubble
		# note: initial impage.pos are 0,0 until next clock cycle
		def tmp(page, dt): page.load_boxes(hidden=hidden) # discard dt
		for pg in self.im_pages:
			Clock.schedule_once(functools.partial(tmp, pg), 0)

		return self

	@property
	def on_double_click(self): return ImPage.on_double_click


if __name__ == "__main__":
	from kivy.app import App
	from kivy.uix.boxlayout import BoxLayout

	glob_dir = r"C:\scans\Knight Run\225\wr*.png"
	chap_num= 225

	pages= Page.load_pages(series="knight", chap_num=chap_num, glob_dir=glob_dir)

	class TestApp(App):
		def build(self):
			self.root = BoxLayout()

			viewer = Viewer()
			self.root.add_widget(viewer)
			viewer.build(pages, hidden=False)

			return self.root


	kivy_utils.doFullScreen()
	a = TestApp()
	a.run()
