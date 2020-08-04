from kivy.config import Config
from kivy.uix.textinput import TextInput

Config.set('kivy', 'log_level', 'debug')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelItem
import cv2

kv = """
<InOne>:
    text: "one"

<InTwo>:
	text: "two"

<Test>:
	orientation: "vertical"
	
	Label:
		text: "Default Label"
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
		self.root.populate(num=5)
		return self.root

if __name__ == '__main__':
	TestApp().run()