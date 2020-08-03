import utils
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty, NumericProperty, ListProperty

Builder.load_file(utils.KIVY_CLASS_DIR + "translation_table_layout.kv")

class Row(BoxLayout):
	on_focus= [] # @TODO: rename on_focus to on_click
	on_double_click= []

	def build(self, row_index, kor="", eng=""):
		self.row_index= int(row_index) # Row Index @TODO: prevent duplicate indices?

		self.num= RowLabel(text=str(self.row_index)) # Label for row number (1-indexed, ignoring header row)
		self.kor= KorInput(text=kor) # TextInput for Korean
		self.eng= EngInput(text=eng) # TextInput for English

		self.add_widget(self.num)
		self.add_widget(self.kor)
		self.add_widget(self.eng)

		return self

	# click events
	def on_touch_down(self, touch):
		if self.collide_point(*touch.pos) and self.on_focus:
			if touch.button == "left":
				self.on_focus(self)
		return super().on_touch_down(touch)


class TranslationTable(ScrollView):
	rows= ListProperty()
	row_height= NumericProperty(60)

	# Add to or regenerate the table entries
	def build(self, row_height=None, clear=True, on_focus=None):
		if clear:
			if self.rows: self.layout.clear_widgets(self.rows) # Falsy values will clear ALL children
			self.rows= []
			self.pages_bubbles_rows= []
		if on_focus: Row.on_focus= on_focus

		self.layout= self.ids.layout # BoxLayout
		if row_height: self.row_height= row_height

		for x in self.rows: self.layout.add_widget(x)
		return self

	def append_row(self, kor="", eng=""):
		r= Row().build(row_index=len(self.rows)+1, kor=kor, eng=eng)
		self.rows.append(r)
		self.layout.add_widget(r)

		return r

	def insert_row(self, index, kor="", eng=""):
		r= Row().build(row_index=index, kor=kor, eng=eng)
		self.rows.insert(index, r)
		self.build(clear=False)

		return r

	def populate_from_pages(self, pages, on_focus=None):
		self.build(on_focus=on_focus)

		for pg in pages:
			for bubb in pg.bubbles:
				r= self.append_row(kor=bubb.raw_text)
				self.pages_bubbles_rows.append({"bubble": bubb, "row": r, "page": pg})

	@property
	def on_focus(self): return Row.on_focus

	@property
	def on_double_click(self): return Row.on_double_click

class KorInput(TextInput): pass
class EngInput(TextInput): pass
class RowLabel(Label): pass
class HeaderLabel(Label): pass


if __name__ == "__main__":
	from kivy.app import App

	class TestApp(App):
		def build(self):
			self.root= BoxLayout()

			tbl= TranslationTable().build()
			for i in range(20): tbl.append_row()

			self.root.add_widget(tbl)

			return self.root

	a= TestApp()
	a.run()