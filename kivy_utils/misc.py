import functools, numpy as np

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand') # Disable multi-touch


# rel_y: Vertical distance from bottom-corner of window (Kivy's y)
# scroll_y: How far scrollbar from top [0,1]
def getAbsY(rel_y, scroll_y, heights):
	totalHeight= sum(heights)
	return (1-scroll_y)*(totalHeight-Window.height) +  Window.height-rel_y

# Returns y-pos relative to top-left of current page (PAGE =/= WINDOW)
def getPgY(abs_y, pageNum, heights):
	for i in range(pageNum):
		abs_y-= heights[i]
	return abs_y

# abs_y: Vertical distance from top-left corner of first page
def getPageNum(abs_y, heights):
	for i in range(len(heights)):
		abs_y-= heights[i]
		if abs_y < 0: return i
	return len(heights)-1

def doFullScreen():
	Window.maximize()
	size= Window.size
	Window.restore()

	Config.set('graphics', 'width', size[0])
	Config.set('graphics', 'height', size[1])
	Window.size= size
	Window.top= 23+3
	Window.left= 0


schedule= {}
def __wait(instance,value, func, delay=0.5, **kwargs):
	global schedule
	iid= str(id(instance))

	if iid not in schedule:
		schedule[iid]= Clock.schedule_once(lambda x: func(instance,value, **kwargs), delay)
	else:
		schedule[iid].cancel()
		schedule[iid]= Clock.schedule_once(lambda x: func(instance,value, **kwargs), delay)

def wait(func, delay=0.5, **kwargs):
	return functools.partial(__wait, func=func, delay=delay, **kwargs)


def within(x, y, bbox, margin=5):
	return (bbox['x']-margin <= x <= bbox['x']+bbox['w']+margin)\
	   and (bbox['y']-margin <= y <= bbox['y']+bbox['h']+margin)


# p_x: x coord rel. to top-left of page
def getWordLine(p_x, p_y, ocr_data):
	l,w,wbb,lbb= (None,)*4

	for line,lb in ocr_data:
		for word,wb in line:
			if within(p_x, p_y, wb):
				w= word
				wbb=wb

		# print(x,y,"\t",[z[0] + "\t" + ','.join([str(z[1][zz]) for zz in z[1]]) for z in line])
		if within(p_x, p_y, lb):
			l= " ".join([z[0] for z in line])
			lbb= lb

	return w,l,wbb,lbb


def modBox(bbox, bb, pg_y, rel_y, pad=None):
	tmp= [abs(bb['w']), abs(bb['h'])]
	if pad is None: pad= int(min(tmp) / 7)

	bbox.pos= (bb['x'], pg_y-bb['y']+rel_y)
	bbox.size= (bb['w'], -bb['h'])

	bbox.pos= (-pad + bbox.pos[0], pad+bbox.pos[1])
	bbox.size= (np.sign(bbox.size[0])*pad*2 + bbox.size[0], np.sign(bbox.size[1])*pad*2 + bbox.size[1])

	return bbox