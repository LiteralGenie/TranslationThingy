from kivy.config import Config
from kivy.properties import ObjectProperty, DictProperty

Config.set('kivy', 'log_level', 'debug')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelItem

import utils
Builder.load_file(utils.KIVY_CLASS_DIR + "vocab_tabs_layout.kv")

class TabV(TabbedPanelItem):
	def build(self, name):
		self.text= name
		self.layout= GridLayout()
		return self


class VocabPanel(TabbedPanel):
	tabs= DictProperty()
	pinTab= ObjectProperty(None)
	allTab= ObjectProperty(None)

	def build(self):
		self.tabs= {}

		self.pinTab= TabV().build("Pins")
		self.allTab= TabV().build("All")

		self.add_widget(self.pinTab)
		self.add_widget(self.allTab)

		return self

	def add_tab(self, name):
		if name in self.tabs: del self.tabs[name]

		new_tab= TabV().build(name)
		self.tabs[name]= (new_tab)
		self.add_widget(new_tab)

if __name__ == "__main__":
	from kivy.app import App

	class TestApp(App):
		def build(self):
			self.root= BoxLayout()
			self.root.add_widget(VocabPanel().build())
			return self.root

	a= TestApp()
	a.run()