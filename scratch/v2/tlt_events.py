import warnings, kivy_utils, numpy as np
from kivy.app import App


# highlight sentence on table click
def highlight_bubble(row, padding=None):
	root= App.get_running_app()

	# Get page / bubble / row relevant to clicked row
	dct= None
	for x in root.pages_bubbles_rows:
		if x["row"] is row: dct= x
	if not dct:
		warnings.warn(f"Grouping with Row not found: {str(row)}")
		return

	# Get visible page data
	visible_pages= kivy_utils.get_visible_page_heights(viewer=root.viewer)
	if not any([x['index']+1 == dct['page'].page_num for x in visible_pages]): # bbox not on visible pages
		return

	# Draw bounding box
	draw_box(page=dct['page'], bubble=dct['bubble'],
			 visible_pages=visible_pages,
			 viewer=root.viewer, bubbBox=root.bubbBox)

def draw_box(page, bubble, visible_pages, viewer, bubbBox, padding=None):
	bbox= bubble.bbox
	pos= [bbox['x'], bbox['y']]
	size= [bbox['w'], bbox['h']]

	for x in visible_pages:
		if x['index']+1 != page.page_num:
			pos[1]+= x['end']-x['start'] # earlier pages shift bbox down
		else:
			pos[1]-= x['start'] # container page may be cut off at top, in which case, shift bbox up
			break

	# Flip y
	pos[1]= viewer.height - pos[1]
	size[1]= -size[1]

	# Padding
	if padding is None:
		tmp= [abs(bbox['w']), abs(bbox['h'])]
		padding= int(min(tmp) / 7)

	pos= (-padding + pos[0], padding+pos[1])
	size= (np.sign(size[0])*padding*2 + size[0], np.sign(size[1])*padding*2 + size[1])

	bubbBox.rectangle= pos + size

# remove highlight on scroll
def remove_box(window, pos):
	App.get_running_app().bubbBox.rectangle= (0,)*4