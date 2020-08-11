import kivy_utils # call builder for below classes
from kivy.graphics import Line, Color, InstructionGroup
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import AsyncImage
from kivy.properties import ObjectProperty, NumericProperty, ListProperty

from utils.page_utils import Page
import cv2, glob, utils, functools, math


class Viewer(ScrollView):
	layout = ObjectProperty()
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
		self.layout.height = sum(self.im_heights)

		w= self.bar_width + max([ x.width for x in self.im_pages ])
		self.width= self.layout.width= w

		# draw bbox for each bubble
		# note: initial impage.pos are 0,0 until next clock cycle
		def tmp(page, dt): page.load_boxes(hidden=hidden) # discard dt
		for pg in self.im_pages:
			Clock.schedule_once(functools.partial(tmp, pg), 0)

		return self

	@property
	def on_double_click(self): return ImPage.on_double_click


class ImPage(AsyncImage):
	on_double_click= []

	page = ObjectProperty()
	line_box_color= ListProperty()
	line_width= NumericProperty()
	focus_box_color= ListProperty()
	fade_time= NumericProperty()
	fade_cycles= NumericProperty(1)

	def build(self, page, im_path, page_index):
		im = cv2.imread(im_path)
		LineBox.LINE_WIDTH= self.line_width # janky but kvlang doesnt support rules for instructions

		self.source=im_path
		self.size=tuple(reversed(im.shape[:2]))
		self.bind(texture= self._disable_interplotation)  # Prevent blurring

		self.page= page

		return self

	def load_boxes(self, hidden=True):
		self.boxes= []

		for bubb in self.page.bubbles:
			box= LineBox(color=self.line_box_color).from_bubble(self, bubble=bubb, hidden=hidden)
			self.canvas.after.add(box)
			self.boxes.append(box)

		return self

	# click events
	def on_touch_down(self, touch):
		if touch.button == "left" and touch.is_double_tap:
			for b in self.boxes:
				x_bnds= [b.pos[0], b.pos[0]+b.size[0]]
				y_bnds= [b.pos[1], b.pos[1]+b.size[1]]
				x_bnds.sort(), y_bnds.sort()

				if x_bnds[0] <= touch.pos[0] <= x_bnds[1] \
					and y_bnds[0] <= touch.pos[1] <= y_bnds[1]:
					for func in ImPage.on_double_click: func(b)

		return super().on_touch_down(touch)

	@classmethod
	def _disable_interplotation(cls, image, texture):
		if not texture: return
		image.texture.min_filter = 'nearest'
		image.texture.mag_filter = 'nearest'


class LineBox(InstructionGroup):
	LINE_WIDTH= None

	def __init__(self, color, **kwargs):
		super().__init__(**kwargs)

		self.color= Color(rgba=color)
		self.add(self.color)

		self.box= Line(width= self.LINE_WIDTH)
		self.add(self.box)

		self.hidden= False

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
		self.pos= [-padding + self.pos[0], padding+self.pos[1]]
		self.size= [size_sign[0]*padding*2 + self.size[0], size_sign[1]*padding*2 + self.size[1]]

		self.box.rectangle= self.pos + self.size
		if hidden: self.hide()
		return self

	def hide(self): self.box.rectangle= self.pos + [0,0]; self.hidden= True
	def show(self): self.box.rectangle= self.pos + self.size; self.hidden= False


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
