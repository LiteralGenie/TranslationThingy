import functools, numpy as np

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand') # Disable multi-touch


# rel_y: Vertical distance from bottom-corner of window (Kivy's y)
# scroll_y: How far scrollbar from top [0,1]
def get_y_abs_top(rel_y, scroll_y, heights):
	totalHeight= sum(heights)
	return (1-scroll_y)*(totalHeight-Window.height) +  Window.height-rel_y

# Returns y-pos relative to top-left of current page (PAGE =/= WINDOW)
def get_y_pg_top(y_abs_top, pageNum, heights):
	ret= y_abs_top
	for i in range(pageNum):
		ret-= heights[i]
	return ret

# abs_y: Vertical distance from top-left corner of first page
def getPageNum(y_abs_top, heights):
	ret= y_abs_top
	for i in range(len(heights)):
		ret-= heights[i]
		if ret < 0: return i
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


# Schedule a function call. Refresh the delay if the function is scheduled again.
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

def get_visible_page_heights(viewer):
	ret= []

	scroll_y= viewer.scroll_y
	total_height= sum(viewer.im_heights)
	abs_y_top= round((1-scroll_y)*(total_height-viewer.height)) # distance of top-edge of viewer from top of container


	tmp= 0 # running total of page heights
	start_page= 0 # first visible page in viewer
	for i in range(len(viewer.im_heights)):
		if tmp + viewer.im_heights[i] > abs_y_top: # if page goes below top-edge of viewer...
			start_page= i
			start_height= tmp
			break # this should always be reachable since there should always be a page in the viewer
		else: tmp += viewer.im_heights[i]


	# get heights of visible pages
	rem_height= viewer.height # remaining viewer height
	for i in range(start_page, len(viewer.im_heights)):
		partial_height= start_height + viewer.im_heights[i] - abs_y_top # partial page height

		st= abs_y_top - start_height
		if partial_height >= rem_height: # if partial height exceeds remaining viewer height...
			end= st + rem_height
			ret.append({ "index": i, "start": st, "end": end, "page_height": viewer.im_heights[i] })
			break
		else:
			end= st + partial_height
			ret.append({ "index": i, "start": st, "end": end, "page_height": viewer.im_heights[i] })

		start_height+= viewer.im_heights[i]
		abs_y_top= start_height
		rem_height-= partial_height

	return ret


# Move bbox overlay to new coordinates
# bb: new bbox coords (relative to top-left of containing page)
# pg_y: mouse position (relative to top-left of containing page)
# rel_y: mouse position (relative to top-left of viewer)
def modBox(bbox, bb, pg_y, rel_y, pad=None):
	tmp= [abs(bb['w']), abs(bb['h'])]
	if pad is None: pad= int(min(tmp) / 7)

	pos= (bb['x'], pg_y-bb['y']+rel_y) # Bottom-left corner of bbox
	size= (bb['w'], -bb['h']) # Expand right and up

	# Padding
	pos= (-pad + pos[0], pad+pos[1])
	size= (np.sign(size[0])*pad*2 + size[0], np.sign(size[1])*pad*2 + size[1])

	# Rectangle
	# bbox.pos= pos
	# bbox.size= size

	# Line-Rectangle
	bbox.rectangle= pos + size

	return bbox

# @TODO: rename rel_y and abs_y to show that they're both absolute container coordinates -- rel_y uses top-left as origin -- abs_y uses bottom-left