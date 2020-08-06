import functools, numpy as np

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand') # Disable multi-touch

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


def get_visible_page_heights(viewer): # @TODO: break into reusable chunks
	ret= []

	scroll_y= viewer.scroll_y
	total_height= sum(viewer.im_heights)
	abs_y_top= round((1-scroll_y)*(total_height-viewer.height)) # distance of top-edge of viewer from top of container


	tmp= 0 # running total of page heights
	start_page= 1 # first visible page in viewer
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
			ret.append({ "index": i, "start": st, "end": end })
			break
		else:
			end= st + partial_height
			ret.append({ "index": i, "start": st, "end": end })

		start_height+= viewer.im_heights[i]
		abs_y_top= start_height
		rem_height-= partial_height

	return ret

