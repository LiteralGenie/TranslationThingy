from utils import kivy_utils # call builder for below classes
from kivy.properties import ObjectProperty, NumericProperty, ListProperty
from kivy.uix.image import AsyncImage
from .line_box import LineBox
import cv2


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
			box,lbl= LineBox(color=self.line_box_color).build(self, bubble=bubb, hidden=hidden)
			self.canvas.after.add(box)
			self.boxes.append(box)
			self.add_widget(lbl)
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