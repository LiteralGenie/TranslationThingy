from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
from kivy.effects.scroll import ScrollEffect
from kivy.uix.image import AsyncImage
from kivy.uix.gridlayout import GridLayout

import cv2, glob, utils
from utils.ocr_utils import gapi as api
Builder.load_file(f'{utils.KIVY_CLASS_DIR}/viewer_layout.kv')

class Viewer(ScrollView):
	def build(self, globDir=None, chapNum=None, series="Knight"):
		self.grid= GridLayout(cols=1, size_hint=(None,None), size=(0,0))
		self.imPaths= []
		self.im_heights= []
		self.ocr_data= []

		self.add_widget(self.grid)
		if globDir: self.addImages(glob.glob(globDir), chapNum=chapNum, series=series)

		return self

	def addImages(self, imPaths, chapNum=None, series=None):
		self.imPaths+= imPaths

		def _disable_interplotation(image, texture):
			if not texture: return
			image.texture.min_filter = 'nearest'
			image.texture.mag_filter = 'nearest'

		for i,p in enumerate(imPaths):
			im= cv2.imread(p)
			x= AsyncImage(	source=p,
							size_hint=(None,None),
							size= tuple(reversed(im.shape[:2])))
			x.bind(texture=_disable_interplotation) # Prevent blurring

			self.grid.add_widget(x)
			self.grid.height+= im.shape[0]
			self.width= self.grid.width= max(self.grid.width, im.shape[1]+10)
			self.im_heights+= [im.shape[0]]

			name= None
			if chapNum is not None and series is not None:
				name= api.get_name(series=series, chapter=chapNum, page=i+1)
			self.ocr_data.append(api.ocr(p, name=name))
