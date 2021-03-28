from utils import kivy_utils # call builder for below classes
from kivy.graphics import Line, Color, InstructionGroup
from .bubble_label import BubbleLabel


class LineBox(InstructionGroup):
	LINE_WIDTH= None

	def __init__(self, color, **kwargs):
		super().__init__(**kwargs)

		self.color= Color(rgba=color)
		self.add(self.color)

		self.box= Line(width= self.LINE_WIDTH)
		self.add(self.box)

		self.hidden= False

	def build(self, im_page, bubble, hidden=True, padding=None):
		box= self._get_box(im_page, bubble, padding=padding)
		lbl= self._get_label(im_page, bubble)

		if hidden: self.hide()
		return box,lbl

	def _get_label(self, im_page, bubble):
		lbl= BubbleLabel().build(im_page, bubble)
		self.label= lbl

		return lbl

	def _get_box(self, impage, bubble, padding=None):
		self.bubble= bubble
		self.pos, self.size= kivy_utils.get_bubble_coords(impage, bubble, padding=padding)
		self.box.rectangle= self.pos+self.size
		return self

	def hide(self):
		self.box.rectangle= self.pos + [0,0]
		self.label.color= [0,0,0,0]
		self.hidden= True
	def show(self):
		self.box.rectangle= self.pos + self.size
		self.label.color= self.label.normal_color
		self.hidden= False

