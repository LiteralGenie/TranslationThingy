from utils import kivy_utils # calls builder exactly once
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App

class TableButtons(BoxLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def build(self):
		self.toggle_box_button.bind(on_press=toggle_boxes)

def toggle_boxes(button):
	app= App.get_running_app()

	for im_page in app.viewer.im_pages:
		for box in im_page.boxes:
			if button.state == "down": box.show()
			elif button.state == "normal": box.hide()