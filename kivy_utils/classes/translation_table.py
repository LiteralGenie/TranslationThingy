import utils
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty, NumericProperty, ListProperty

Builder.load_file(utils.KIVY_CLASS_DIR + "translation_table_layout.kv")

class Row(BoxLayout):
	row_index= NumericProperty(-1) # Row Index @TODO: prevent duplicate indices?
	num= ObjectProperty(None) # Label for row number (0 for header row)
	kor= ObjectProperty(None) # TextInput for Korean
	eng= ObjectProperty(None) # TextInput for English

	def build(self, row_index, kor="", eng=""):
		self.row_index= int(row_index)

		self.num= RowLabel(text=str(self.row_index))
		self.kor= KorInput(text=kor)
		self.eng= EngInput(text=eng)

		self.add_widget(self.num)
		self.add_widget(self.kor)
		self.add_widget(self.eng)

		return self


class TranslationTable(ScrollView):
	rows= ListProperty()
	num_rows= NumericProperty(0)
	row_height= NumericProperty(40)

	def build(self, num_rows=1, row_height=None):
		self.rows= []
		self.layout= self.ids.layout # BoxLayout
		self.num_rows= num_rows
		if row_height: self.row_height= row_height

		for i in range(num_rows): self.rows.append(Row().build(row_index=i+1))
		for x in self.rows: self.layout.add_widget(x)

		return self


class KorInput(TextInput): pass
class EngInput(TextInput): pass
class RowLabel(Label): pass
class HeaderLabel(Label): pass


if __name__ == "__main__":
	from kivy.app import App

	class TestApp(App):
		def build(self):
			self.root= BoxLayout()
			self.root.add_widget(TranslationTable().build(num_rows=30))
			return self.root

	a= TestApp()
	a.run()