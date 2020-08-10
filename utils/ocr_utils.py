import requests, os, abc, utils, io, re
from google.cloud import vision

CONFIG= utils.loadJson(utils.CONFIG_DIR + "azure_creds.json")

class api(abc.ABC):
	def __init__(self, image_path):
		self.image_path= image_path
		assert os.path.exists(image_path), "Invalid image path."

	@classmethod
	def ocr(cls, image_path, online=True, name=None, verbose=True):
		if not name: name= os.path.basename(image_path).split(".")[0]

		outFile= utils.OCR_DIR + str(name.lower()) + ".json"

		if os.path.exists(outFile):
			ret= utils.loadJson(outFile)
		elif online:
			if verbose: print("Scanning", image_path, "...")
			api= cls(image_path)
			api.doRequest()
			api.extract()
			#@TODO: cache api responses

			ret= api.texts
			utils.dumpJson(ret, outFile)
		else: return []

		return ret

	@classmethod
	def get_name(cls, series, chapter, page): # page should be 1-indexed
		assert page > 0, "Page numbers when retrieving OCR data should be 1-indexed (because that's how the image is usually named)"
		if any([ x is None for x in [series, chapter, page] ]):
			return None
		return f"{series}_{chapter}-{page}"

	@abc.abstractmethod
	def doRequest(self):
		"""Upload image to API and get response."""
		return

	@abc.abstractmethod
	def extract(self):
		"""Process API response."""
		return

	@staticmethod
	def _clean(text):
		ret= text
		subs= {
			"regex": { "chars": [r"[^\w\.',?!<>]"], "reps": [""] },
			"unicode": {"chars": [r"\u"], "reps": ["&#x"]}
		}
		for group in subs:
			for char in subs[group]['chars']:
				for rep in subs[group]['reps']:
					if group == "regex": ret= re.sub(char, rep, ret)
					else: ret= ret.replace(char, rep)

		return ret

	# def render(self, fontSize=15):
	# 	matplotlib.use("TkAgg")
	#
	# 	fp= matplotlib.font_manager.FontProperties(fname = r'F:\downloads_trash\NanumBarunGothic.ttf', size=fontSize)
	#
	# 	# Display the image and overlay it with the extracted text.
	# 	plt.figure(figsize=(10, 10))
	# 	image = Image.open(self.image_path)
	# 	ax = plt.imshow(image, alpha=0.5)
	#
	# 	for tuple in self.texts:
	# 		word, bbox= tuple
	# 		origin = (bbox['x'], bbox['y'])
	# 		patch = Rectangle(origin, bbox['w'], bbox['h'],
	# 						  fill=False, linewidth=2, color='y')
	# 		ax.axes.add_patch(patch)
	# 		plt.text(origin[0], origin[1], word, fontproperties=fp, va='top')
	# 	plt.show(block=False)
	# 	plt.axis("off")
	# 	plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

	# def mshow(self):
	# 	plt.show()

	def cshow(self, show=True, file=None):
		import cv2

		im= cv2.imread(self.image_path)
		for lt in self.texts:
			line, bbox= lt
			cv2.rectangle(im, (bbox['x'], bbox['y']), (bbox['x']+bbox['w'], bbox['y']+bbox['h']), (0,0,180), 2)

			for wt in line:
				word, bbox= wt
				cv2.rectangle(im, (bbox['x'], bbox['y']), (bbox['x']+bbox['w'], bbox['y']+bbox['h']), (0,0,180), 2)

		if show:
			cv2.imshow(self.image_path, im)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
		if file:
			cv2.imwrite(file, im)



class msapi(api):
	def doRequest(self):
		ep= CONFIG['endpoint']
		key= CONFIG['key']
		api_url = ep + "vision/v2.1/ocr"

		# Set image_path to the local path of an image that you want to analyze.
		image_path= self.image_path

		# Read the image into a byte array
		image_data = open(image_path, "rb").read()
		headers = {'Ocp-Apim-Subscription-Key': key,
				   'Content-Type': 'application/octet-stream'}
		params = {'visualFeatures': 'Categories,Description,Color'}
		response = requests.post(
			api_url, headers=headers, params=params, data=image_data)
		response.raise_for_status()
		self.response= response.json()

		return self.response

	def extract(self, analysis=None):
		if not analysis: analysis= self.response

		# Extract the word bounding boxes and text.
		self.line_infos= [region["lines"] for region in analysis["regions"]]
		self.texts= []
		for line in self.line_infos:
			words= []
			for word_metadata in line:
				for word_info in word_metadata["words"]:
					b= [int(x) for x in word_info['boundingBox'].split(",")]
					bbox= {"x": b[0], "y": b[1], "w": b[2], "h": b[3]}
					words.append((word_info['text'], bbox))

			x= min([x[1]['x'] for x in words])
			y= min([y[1]['y'] for y in words])
			w= max([x[1]['x'] + x[1]['w'] for x in words])-x
			h= max([y[1]['y'] + y[1]['h'] for y in words])-y
			bbox= {"x": x, "y": y, "w": w, "h": h}
			self.texts.append((words, bbox))

		return self.texts


class gapi(api):
	def doRequest(self):
		client= vision.ImageAnnotatorClient.from_service_account_json(utils.CONFIG_DIR + "gcreds.json")
		content= io.open(self.image_path, 'rb').read()
		image = vision.types.Image(content=content)

		self.response = client.text_detection(image=image)
		return self.response

	@staticmethod
	def _getBbox(verts):
		x= min([v.x for v in verts])
		y= min([v.y for v in verts])
		width= max([v.x for v in verts]) - x + 1
		height= max([v.y for v in verts]) - y + 1

		return {"x": x, "y": y, "w": width, "h": height}

	def extract(self):
		self.texts= []

		# for text in self.response.text_annotations[1:]:
		# 	t= gapi.clean(text.description)
		# 	verts= text.bounding_poly.vertices
		#
		# 	x= min([v.x for v in verts])
		# 	y= min([v.y for v in verts])
		# 	width= max([v.x for v in verts]) - x + 1
		# 	height= max([v.y for v in verts]) - y + 1
		#
		# 	self.texts.append((t, {"x": x, "y": y, "w": width, "h": height}))

		for pg in self.response.full_text_annotation.pages:
			for blk in pg.blocks:
				for para in blk.paragraphs:
					words= []
					for w in para.words:
						word= ''.join([gapi._clean(x.text) for x in w.symbols])
						if word:
							bbox= gapi._getBbox(w.bounding_box.vertices)
							words.append((word, bbox))

					bbox= para.bounding_box.vertices
					self.texts.append((words, gapi._getBbox(bbox)))

		return self.texts