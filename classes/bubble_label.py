from utils import kivy_utils # call builder for below classes
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, NumericProperty, ListProperty
from kivy.clock import Clock


class BubbleLabel(Label):
	dist= NumericProperty()

	def build(self, im_page, bubble):
		def get_bounds(val, size):
			ret= [val, val+size]
			ret.sort()
			return ret

		self.num= bubble.num
		self.text= str(self.num+1)

		pos,size= kivy_utils.get_bubble_coords(im_page, bubble)
		side= "top" if pos[1] > 2*self.dist else "bot" # text above or below box
		self.pos[0]= pos[0] + size[0]//2

		def reposition(dt): self.pos[0]-= self.texture_size[0]//2 # texture_size 0 until added
		Clock.schedule_once(reposition,0)

		y_bnds= get_bounds(pos[1], size[1])
		if side == "top": self.pos[1]= y_bnds[1] + self.dist
		elif side == "bot": self.pos[1]= y_bnds[0] - self.dist

		return self
