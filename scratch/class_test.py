from kivy.config import Config
from kivy.uix.textinput import TextInput

Config.set('kivy', 'log_level', 'debug')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.base import EventLoop
import kivy_utils

kv = """
<InOne>:
    text: "one"

<InTwo>:
	text: "two"

<Test>:
	orientation: "vertical"	
"""
Builder.load_string(kv)

class InOne(TextInput):
	pass

class InTwo(TextInput):
	pass

class Test(BoxLayout):
	def populate(self):
		self.add_widget(InOne())
		self.add_widget(InTwo())
		return self

class TestApp(App):
	def build(self):
		self.root= Test().populate()
		return self.root

if __name__ == '__main__':
	TestApp().run()