from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
from kivy.effects.scroll import ScrollEffect
from kivy.uix.image import AsyncImage
from kivy.uix.gridlayout import GridLayout

import cv2, glob, utils

from utils.ocr_utils import gapi as api

class Viewer(ScrollView):
	def __init__(self, globDir=None, chapNum=None, series="Knight"):
		Builder.load_file(f'{utils.PROJECT_DIR}kivy_utils/classes/viewer_layout.kv')

		super().__init__(
						 	# effect_cls=ScrollEffect,
							 )
		# self.effect_cls.friction= 0.2

		self.grid= GridLayout(cols=1, size_hint=(None,None), size=(0,0))
		self.imPaths= []
		self.heights= []
		self.ocr_data= []

		self.add_widget(self.grid)
		if globDir: self.addImages(glob.glob(globDir), chapNum=chapNum, series=series)

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
			self.heights+= [im.shape[0]]

			name= None
			if chapNum is not None and series is not None:
				name= f"{series}_{chapNum}-{i+1}"
			self.ocr_data.append(api.ocr(p, name=name))
