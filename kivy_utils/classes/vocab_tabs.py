from kivy.config import Config
from kivy.properties import ObjectProperty, DictProperty, StringProperty

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

class WordCard(GridLayout):
	name= StringProperty()

	def build(self, data):
		self.ids.name.text= data['name']

		return self

class TabV(TabbedPanelItem):
	layout= ObjectProperty(None)
	words= DictProperty()

	def build(self, name, words=None):
		self.text= name
		self.layout= self.ids.layout

		if words: self.add_words(words)
		return self

	def add_words(self, words):
		self.layout.cols= 10

		for x in words:
			self.words[x]= words[x]

		self.clear_widgets()
		for x in sorted(self.words.keys(), key=lambda y: words[y]['name']):
			self.layout.add_widget(WordCard().build(words[x]))

	def remove_words(self, words):
		tmp= []
		for x in words:
			for y in self.words:
				if x['name'] == y['name']:
					tmp.append(y)

		for y in tmp: del self.words[y]

	def clear_words(self):
		self.words= {}
		self.clear_widgets()

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

	def add_tab(self, name, data):
		if name in self.tabs: del self.tabs[name]

		new_tab= TabV().build(name)
		self.tabs[name]= (new_tab)
		self.add_widget(new_tab)

if __name__ == "__main__":
	from kivy.app import App

	class TestApp(App):
		def build(self):
			self.root= BoxLayout()

			vocab= VocabPanel().build()
			vocab.pinTab.add_words({
				"1": { "name": "aaa" },
				"2": { "name": "ccc" },
				"3": { "name": "bbb" },
				"4": { "name": "eee" },
				"5": { "name": "ddd" },
			})

			self.root.add_widget(vocab)
			return self.root

	a= TestApp()
	a.run()