import kivy_utils # call builder for below classes
from kivy.graphics import Line, Color
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import AsyncImage
from kivy.properties import ObjectProperty, NumericProperty
from utils.page_utils import Page

import cv2, glob, utils, functools, math


class Viewer(ScrollView):
	layout = ObjectProperty()
	overlay= ObjectProperty()

	def build(self, glob_dir=None, chap_num=None, series="Knight", hidden=True):
		self.im_paths = []
		self.pages= []
		self.im_heights= []

		if glob_dir: self.load_images(glob.glob(glob_dir), chap_num=chap_num, series=series, hidden=hidden)

		return self

	def load_images(self, im_paths, chap_num=None, series=None, hidden=True):
		self.im_paths= im_paths

		for i, p in enumerate(im_paths):
			pg= ImPage().build(overlay_canvas=self.layout.canvas,
			                   im_path=p,
			                   page_index=i + 1,
			                   series=series,
			                   chap_num=chap_num)

			self.layout.add_widget(pg)
			self.pages.append(pg)

		self.im_heights= [x.height for x in self.pages]
		self.layout.height = sum(self.im_heights)

		w= self.bar_width + max([ x.width for x in self.pages ])
		self.width= self.layout.width= w

		# initial pos are 0,0 until next clock cycle
		def tmp(page, dt): page.load_rects(hidden=hidden) # discard dt
		for pg in self.pages:
			Clock.schedule_once(functools.partial(tmp, pg), 0)

		return self


class ImPage(AsyncImage):
	page = ObjectProperty()
	rects = ObjectProperty()
	line_box_color= ObjectProperty()
	line_width= NumericProperty()

	def build(self, im_path, page_index, overlay_canvas, series=None, chap_num=None):
		im = cv2.imread(im_path)
		LineBox.LINE_WIDTH= self.line_width # janky but kvlang doesnt support rules for instructions

		self.source=im_path
		self.size=tuple(reversed(im.shape[:2]))
		self.overlay_canvas= overlay_canvas
		self.bind(texture= self._disable_interplotation)  # Prevent blurring

		self.page= Page(im_path=im_path, page_num=page_index, chap_num=chap_num, series=series)
		self.page.load_bubbles()

		return self

	def load_rects(self, hidden=True):
		self.rects= []

		for bubb in self.page.bubbles:
			with self.overlay_canvas.after:
				Color(*self.line_box_color)
				lb= LineBox().from_bubble(self, bubb, hidden=hidden)
				self.rects.append(lb)

		return self

	@classmethod
	def _disable_interplotation(cls, image, texture):
		if not texture: return
		image.texture.min_filter = 'nearest'
		image.texture.mag_filter = 'nearest'


class LineBox(Line):
	has_focus= False
	LINE_WIDTH= 99

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.width= self.LINE_WIDTH

	def from_bubble(self, impage, bubble, hidden=True, padding=None):
		bbox= bubble.bbox

		# kivy origin is at bottom left. cv2 origin is at top left.
		self.pos= [bbox['x'], impage.height-bbox['y']+impage.pos[1]]
		self.size= [bbox['w'], -bbox['h']]
		self.bubble= bubble

		# padding
		if padding is None:
			tmp= [abs(bbox['w']), abs(bbox['h'])]
			padding= int(min(tmp) / 7)

		size_sign= [abs(self.size[0]) // self.size[0] , abs(self.size[1]) // self.size[1]]
		self.pos= (-padding + self.pos[0], padding+self.pos[1])
		self.size= (size_sign[0]*padding*2 + self.size[0], size_sign[1]*padding*2 + self.size[1])

		self.rectangle= self.pos + self.size
		if hidden: self.hide()
		return self

	def hide(self): self.rectangle= self.pos + [0,0]

	def show(self): self.rectangle= self.pos + self.size


if __name__ == "__main__":
	from kivy.app import App
	from kivy.uix.boxlayout import BoxLayout

	glob_dir = r"C:\scans\Knight Run\225\wr*.png"
	chap_num= 225

	class TestApp(App):
		def build(self):
			self.root = BoxLayout()

			viewer = Viewer()
			self.root.add_widget(viewer)
			viewer.build(glob_dir=glob_dir, chap_num=chap_num, series="knight", hidden=False)

			return self.root


	kivy_utils.doFullScreen()
	a = TestApp()
	a.run()
