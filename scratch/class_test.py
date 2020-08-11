from kivy.config import Config
Config.set('kivy', 'log_level', 'debug')

from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.animation import Animation

import functools

kv = """
<MyWidget>:
"""
Builder.load_string(kv)

class MyWidget(BoxLayout):
	def populate(self):
		self.l= Label(text="test", color=[1,1,1,1])
		self.add_widget(self.l)

		button= Button(text="change color")
		def tmp(instance):
			a= Animation(color=[1,0,0,1], duration=1)
			a.start(instance.parent.l)
		button.bind(on_press=tmp)
		self.add_widget(button)

		return self


class TestApp(App):
	def build(self):
		return MyWidget().populate()

if __name__ == '__main__':
	a=TestApp()
	a.run()