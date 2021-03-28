import cv2, numpy, os, json

def preprocess(img, blur=True, grey=True):
	ret= numpy.copy(img)
	if blur: ret= cv2.GaussianBlur(img, (3,3), 0)
	if grey: ret= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	return ret

def doAdaptiveCanny(img):
	tMax, __ = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	tMin= tMax / 2

	# print(tMin, tMax)
	return cv2.Canny(img, tMin, tMax, L2gradient=True)

def getFilteredCtrs(ctrs):
	filtered = []
	for c in ctrs:
		x, y, w, h = cv2.boundingRect(c)
		if w * h < 2500 or w < 20 or h < 20 or cv2.arcLength(c, False) < 300: continue
		filtered.append(c)
	return filtered

def getCropped(im, ctrs, margin=30):
	cropped= []
	for c in ctrs:
		x,y,w,h= cv2.boundingRect(c)

		x-= margin
		y-= margin
		w+= margin*2
		h+= margin*2

		x= max(x,0)
		y= max(y,0)

		imDims= numpy.shape(im)
		if x+w >= imDims[1]: w= imDims[1]-x-1
		if y+h >= imDims[0]: w= imDims[0]-y-1

		crop= im[y:y+h, x:x+w]
		cropped.append(crop)
	return cropped

def makeDir(savePath):
	if "." in savePath: savePath= os.path.dirname(savePath)
	if not os.path.exists(savePath):
		print("Making", savePath)
		os.makedirs(savePath)
		return True
	return False

def loadJson(path, default=None):
	if not default: default= {}
	data= default

	assert path.lower().endswith(".json")
	if not os.path.exists(path):
		return data
	else:
		try: return json.load(open(path, encoding='utf-8'))
		except json.JSONDecodeError as e:
			print("Not a valid JSON", "|", default, "|", path)
			return data

def dumpJson(dct, path):
	makeDir(path)
	with open(path, "w+", encoding='utf-8') as file:
		json.dump(dct, file, indent=2, ensure_ascii=False)



# Init crawler
def initDriver(headless=True):
	from selenium import webdriver
	from selenium.webdriver.chrome.options import Options
	options = Options()
	options.headless= headless
	driver = webdriver.Chrome(executable_path=r'C:\Programming\TranslationThingy\TranslationThingy\data\chromedriver.exe', options=options)

	return driver