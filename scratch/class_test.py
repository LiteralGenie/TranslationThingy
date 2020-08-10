from kivy.config import Config
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.uix.image import AsyncImage
from kivy.uix.textinput import TextInput

Config.set('kivy', 'log_level', 'debug')

from kivy.graphics import Color, Line
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.base import EventLoop
import kivy_utils

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, NumericProperty
from kivy.graphics import *
from kivy.uix.button import Button
from kivy.clock import Clock

import functools

kv = """
<MyWidget>:
"""
Builder.load_string(kv)

class TestGroup(InstructionGroup):
	def __init__(self, rgba, **kwargs):
		super().__init__(**kwargs)
		self.color= Color(rgba=rgba)
		self.line= Line(points=[0,0,500,500], width=20)

		self.add(self.color)
		self.add(self.line)

class MyWidget(Widget):
	def populate(self):
		# blue line
		self.blue_grp= TestGroup(rgba=[0,0,1, 0.5])
		self.canvas.add(self.blue_grp)

		# red overlay for line
		self.overlay_grp= TestGroup(rgba=[1,0,0, 0])
		self.canvas.add(self.overlay_grp)

		# button to trigger / fade overlay
		button= Button(text="Begin Fade")

		def start(instance):
			overlay_color= instance.parent.overlay_grp.color
			overlay_color.rgba[3]= 1
			Clock.schedule_once(functools.partial(fade, overlay_color), 0)

		# decrement alpha by 2% every 0.1s until a certain threshold
		def fade(color, dt):
			if color.rgba[3] > 0.05:
				color.rgba[3]-= 0.02
				Clock.schedule_once(functools.partial(fade, color), 0.1)
				print("alpha:", round(color.rgba[3],3))
			else: color.rgba[3]= 0

		button.bind(on_press=start)
		self.add_widget(button)

		return self

class TestApp(App):
	def build(self):
		return MyWidget().populate()

if __name__ == '__main__':
	a=TestApp()
	a.run()