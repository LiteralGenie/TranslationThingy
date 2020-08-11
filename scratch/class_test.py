from kivy.config import Config
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.uix.image import AsyncImage
from kivy.uix.textinput import TextInput

Config.set('kivy', 'log_level', 'debug')

from kivy.graphics import Color, Line
from kivy.app import App
from kivy.lang import Builder
from kivy.animation import Animation
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
		self.blue_grp= TestGroup(rgba=[1,0,0, 0.3])
		self.canvas.add(self.blue_grp)

		# red overlay for line
		# self.overlay_grp= TestGroup(rgba=[1,0,0, 0])
		# self.canvas.add(self.overlay_grp)

		# button to trigger / fade overlay
		button= Button(text="Begin Fade")

		anim= Animation(r=1, g=0, b=0, a=0.3, duration=1)

		def start(instance):
			instance.parent.blue_grp.color.rgba= [1,.5,.5,1]
			anim.start(instance.parent.blue_grp.color)
			# overlay_color= instance.parent.overlay_grp.color
			# overlay_color.rgba[3]= 1
			# Clock.schedule_once(functools.partial(fade, overlay_color), 0)

		button.bind(on_press=start)
		self.add_widget(button)

		return self

class TestApp(App):
	def build(self):
		return MyWidget().populate()

if __name__ == '__main__':
	a=TestApp()
	a.run()