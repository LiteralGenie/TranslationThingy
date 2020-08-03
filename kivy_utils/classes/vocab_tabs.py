from kivy.config import Config
from kivy.properties import ObjectProperty, DictProperty, StringProperty, ListProperty

Config.set('kivy', 'log_level', 'debug')

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelItem

import utils
Builder.load_file(utils.KIVY_CLASS_DIR + "vocab_tabs_layout.kv")


"""
word is dict with:
	name - string
	
	
words is list of word
"""


class WordCard(GridLayout):
	name= StringProperty()

	def build(self, word):
		self.ids.name.text= word['name']

		return self


class TabV(TabbedPanelItem):
	layout= ObjectProperty(None)
	words= DictProperty()
	wordWidgets= ListProperty()
	name= StringProperty()

	def build(self, name, words=None):
		self.name= self.text= name
		self.layout= self.ids.layout

		if words: self.add_words(words)
		return self


	def add_words(self, words):
		if self.wordWidgets: self.clear_widgets(self.wordWidgets) # Falsy values will clear ALL children
		self.wordWidgets= []

		for x in words:
			self.words[x['name']]= x

		for x in sorted(words, key=lambda y: y['name']):
			self.wordWidgets.append(WordCard().build(x))

		for x in self.wordWidgets: self.layout.add_widget(x)

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

	def add_tab(self, name, words=None):
		if name in self.tabs: del self.tabs[name]

		new_tab= TabV().build(name, words=words)
		self.tabs[name]= new_tab
		self.add_widget(new_tab)



if __name__ == "__main__":
	from kivy.app import App

	class TestApp(App):
		def build(self):
			self.root= BoxLayout()

			vocab= VocabPanel().build()
			vocab.pinTab.add_words([
				{ "name": "aaa" },
				{ "name": "ccc" },
				{ "name": "bbb" },
				{ "name": "eee" },
				{ "name": "ddd" }
			])

			self.root.add_widget(vocab)
			return self.root

	a= TestApp()
	a.run()

# @TODO: Link "all" tab with other tabs