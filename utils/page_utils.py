import cv2, glob
from utils.ocr_utils import gapi as api
import utils.stitch_utils as stitch_utils

# Zero-indexed!!!!!!!
class Page:
	def __init__(self, page_num, im_path, series=None, chap_num=None):
		self.series= series
		self.chap_num= chap_num
		self.page_num= page_num

		self.im_path= im_path
		self.im= cv2.imread(im_path)
		self.shape= self.im.shape # height, width, channels

		self.bubbles= []

	# chap_num and series can be any identifier but glob_dir should refer to an actual set of images
	@classmethod
	def load_pages(cls, series, chap_num, glob_dir):
		ret= []
		for i,im in enumerate(glob.glob(glob_dir)):
			ret.append(Page(series=series, chap_num=chap_num, page_num=i+1, im_path=im))

		for page in ret:
			page.load_bubbles()

		return ret

	def load_bubbles(self):
		name= api.get_name(series=self.series, chapter=self.chap_num, page=self.page_num)
		ocr_data= api.ocr(self.im_path, name=name)

		for line, lb in ocr_data:
			text= " ".join([word for word,wordBox in line])
			self.bubbles.append(Bubble(raw_text=text, word_data=line, bbox=lb))

		for x in self.bubbles: x.stitch_words()

		return self

	def __eq__(self, other):
		all([x == y for x,y in zip(self.bubbles,other.bubbles)])

	def __str__(self):
		return f"Series [{self.series}] - Chapter [{self.chap_num}] - Page [{self.page_num}]"


class Bubble:
	_count= 0

	def __init__(self, raw_text, bbox, word_data=None):
		"""
		:param bbox: dict(left, top, width, height) relative to top-left corner of page
		:param raw_text: Untranslated text
		"""
		self.bbox= bbox
		self.raw_text= raw_text
		self.word_data= word_data

		self.num= Bubble._count
		Bubble._count+= 1


	def __str__(self):
		return f"{self.raw_text}"

	def stitch_words(self):
		self.word_data= stitch_utils.stitch_words(self.word_data)
		self.raw_text= " ".join(x[0] for x in self.word_data)
		self.bbox= stitch_utils.get_bbox([x[1] for x in self.word_data])
		return self