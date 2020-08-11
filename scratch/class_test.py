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
<Test>:
    size_hint: (None,None)
    orientation: "vertical"
    height: self.minimum_height    
    
<Row>:
	orientation: "horizontal"
	temp: max(t1.minimum_height, t2.minimum_height)
	size_hint: (None,None)
	height: self.minimum_height
	
	TextInput:
		id: t1
		text: "left"
		size_hint: (None,None)
		height: max(self.minimum_height, self.parent.temp)
		
	TextInput:
		id: t2
		text: "right"
		size_hint: (None,None)
		height: max(self.minimum_height, self.parent.temp)
"""

Builder.load_string(kv)

class Row(BoxLayout): pass

class Test(BoxLayout):
	def populate(self):
		for i in range(2): self.add_widget(Row())
		return self

class TestApp(App):
	def build(self):
		return Test().populate()

if __name__ == '__main__':
	a=TestApp()
	a.run()