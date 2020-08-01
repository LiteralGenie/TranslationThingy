from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label



class Widgets(ScrollView):
	def add_labels(self, *args):
		for i in range(20):
			self.ids.box.add_widget(Label(text=str(i)))

Builder.load_file("C:/programming/knightrunreader/scratch/v1/layout.kv")

class SimpleKivy3(App):
	def build(self):
		self.scroll= Widgets()
		Clock.schedule_once(self.scroll.add_labels)
		return self.scroll


if __name__ == "__main__":
	SimpleKivy3().run()