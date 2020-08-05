import kivy_utils
from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
from kivy.uix.recycleview import RecycleView
from kivy.graphics import Line
from kivy.uix.image import AsyncImage
from kivy.properties import ObjectProperty, ListProperty

import cv2, glob, utils
from utils.ocr_utils import gapi as api


class Viewer(RecycleView):
	layout = ObjectProperty()
	im_heights = ListProperty()

	def build(self, globDir=None, chapNum=None, series="Knight"):
		self.imPaths = []
		self.ocr_data = []

		if globDir: self.addImages(glob.glob(globDir), chapNum=chapNum, series=series)

		return self

	def addImages(self, imPaths, chapNum=None, series=None):
		self.imPaths += imPaths

		def _disable_interplotation(image, texture):
			if not texture: return
			image.texture.min_filter = 'nearest'
			image.texture.mag_filter = 'nearest'

		im_widths = []
		for i, p in enumerate(imPaths):
			im = cv2.imread(p)
			x = ImPage(source=p,
			           size=tuple(reversed(im.shape[:2])),
			           nocache=True
			           )
			x.bind(texture=_disable_interplotation)  # Prevent blurring

			self.layout.add_widget(x)
			self.im_heights.append(im.shape[0])
			im_widths.append(im.shape[1])

			name = None
			if chapNum is not None and series is not None:
				name = api.get_name(series=series, chapter=chapNum, page=i + 1)
			self.ocr_data.append(api.ocr(p, name=name))

		self.layout.height = sum(self.im_heights)
		self.width = self.layout.width = max(im_widths) + self.bar_width


class ImPage(AsyncImage):
	page = ObjectProperty()
	rects = ObjectProperty()


class LineBox(Line):
	pass


if __name__ == "__main__":
	from kivy.app import App
	from kivy.uix.boxlayout import BoxLayout

	globDir = r"C:\Users\Anne\Desktop\scans\Father's Day\test/*.png"


	class TestApp(App):
		def build(self):
			self.root = BoxLayout()

			viewer = Viewer().build(globDir=globDir, chapNum=1, series="knight")

			self.root.add_widget(viewer)
			return self.root


	# kivy_utils.doFullScreen()
	a = TestApp()
	a.run()
