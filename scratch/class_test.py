from kivy.config import Config
from kivy.properties import ListProperty

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
<Test>:
	orientation: "vertical"
	
	Label:
		text: "Default Label"
"""
Builder.load_string(kv)

class Test(BoxLayout):
	rows= ListProperty([])

	def populate(self, num=2):
		if self.rows: self.clear_widgets(self.rows)
		self.rows= []

		for i in range(num):
			self.rows.append(Label(text=f"Label {i}"))

		for x in self.rows:
			self.add_widget(x)

		return self

class TestApp(App):
	def build(self):
		self.root= Test().populate()
		self.root.populate(num=5)
		return self.root

if __name__ == '__main__':
	TestApp().run()