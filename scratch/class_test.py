from kivy.config import Config
Config.set('kivy', 'log_level', 'debug')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelItem
import cv2

kv = """
<Test>:
	do_default_tab: False

	TabbedPanelItem:
		text: "Tab 1"
	TabbedPanelItem:
		text: "Tab 2"
"""
Builder.load_string(kv)

class Test(TabbedPanel):
	def build(self):
		pass

class TestApp(App):
	def build(self):
		self.root= Test()
		return self.root

if __name__ == '__main__':
	TestApp().run()