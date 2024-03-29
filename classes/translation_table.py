from classes import TxtInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty, NumericProperty, ListProperty

import utils.papago_utils as MTL

class Row(BoxLayout):
	on_focus= [] # @TODO: rename on_focus to on_click
	on_double_click= []

	num= ObjectProperty(); kor= ObjectProperty(); eng= ObjectProperty()
	row_index= NumericProperty(1)

	def build(self, row_index, kor="", eng="", page=None, bubble=None):
		self.row_index= int(row_index) # Row Index @TODO: prevent duplicate indices?

		self.num.text= str(self.row_index) # Label for row number (1-indexed, ignoring header row)
		self.kor.text= kor # TextInput for Korean
		self.eng.text= eng # TextInput for English

		self.page= page
		self.bubble= bubble

		return self

	# click events
	def on_touch_down(self, touch):

		# TextInput
		for x in [self.kor, self.eng]:
			if x.collide_point(*touch.pos):
				if touch.button == "left":
					for func in Row.on_focus: func(self)

		# double click row label
		for x in [self.num]:
			if x.collide_point(*touch.pos):
				if touch.button == "left" and touch.is_double_tap:
					for func in Row.on_double_click: func(self)

		return super().on_touch_down(touch)


class TranslationTable(ScrollView):
	rows= ListProperty()
	row_height= NumericProperty(60)
	layout= ObjectProperty(None)

	# Add to or regenerate the table entries
	def build(self, clear=True):
		self.layout= self.ids.layout

		if self.rows: self.layout.clear_widgets(self.rows) # Falsy values will clear ALL children
		if clear:
			self.rows= []
			self.pages_bubbles_rows= []

		for x in self.rows: self.layout.add_widget(x)
		return self

	def append_row(self, kor="", eng="", page=None, bubble=None):
		r= Row().build(row_index=len(self.rows)+1, kor=kor, eng=eng, page=page, bubble=bubble)
		if self.rows:
			r.kor.focus_previous= self.rows[-1].eng
			r.kor.focus_next= r.eng
			r.eng.focus_next= StopIteration
		else:
			r.kor.focus_next= r.eng
			r.kor.focus_previous= StopIteration

		self.rows.append(r)
		self.layout.add_widget(r)

		return r

	def insert_row(self, index, kor="", eng=""): pass # @TODO

	def populate_from_pages(self, pages, mtl=False):
		for pg in pages:
			for bubb in pg.bubbles:
				r= self.append_row(kor=bubb.raw_text, page=pg, bubble=bubb)
				if mtl: r.eng.text= MTL.getTranslation(bubb.raw_text)

				self.pages_bubbles_rows.append({"bubble": bubb, "row": r, "page": pg})

	@property
	def on_focus(self): return Row.on_focus

	@property
	def on_double_click(self): return Row.on_double_click


class Div(BoxLayout):
	def build(self, text=""):
		self.text= text


class KorInput(TxtInput): pass
class EngInput(TxtInput): pass
class RowLabel(Label): pass
class HeaderLabel(Label): pass


if __name__ == "__main__":
	from kivy.app import App

	class TestApp(App):
		def build(self):
			self.root= BoxLayout()

			tbl= TranslationTable().build()
			for i in range(3): tbl.append_row(kor=f"kor{i}", eng=f"eng{i}")

			self.root.add_widget(tbl)

			return self.root

	a= TestApp()
	a.run()