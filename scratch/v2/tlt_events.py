import warnings, kivy_utils, numpy as np
from kivy.app import App


# move clicked row into view
def scroll_on_double_click(row, margin_ratio=0.1, padding=None):
	root= App.get_running_app()

	page= row.page
	bubble= row.bubble
	if page is None or bubble is None: return

	tmp= page.page_num
	target_y= sum(root.viewer.im_heights[:tmp])
	target_y+= bubble.bbox['y'] + int(bubble.bbox['h']/2)

	scrollable_dist= sum(root.viewer.im_heights) - root.viewer.height

	target_y-= margin_ratio * root.viewer.height # padding
	target_y= max(0, target_y)
	target_scroll= target_y / scrollable_dist

	root.viewer.scroll_y= 1-target_scroll
	highlight_on_focus(row, padding=padding)


# draw border around text in image
def highlight_on_focus(row, padding=None):
	remove_box()

	root= App.get_running_app()
	page= row.page
	bubble= row.bubble

	# Draw bounding box
	draw_box(page=page, bubble=bubble,
			 viewer=root.viewer, bubbBox=root.bubbBox,
			 padding=padding)


def draw_box(page, bubble, viewer, bubbBox, padding=None):
	bbox= bubble.bbox
	pos= [bbox['x'], bbox['y']]
	size= [bbox['w'], bbox['h']]

	# Get visible page data
	visible_pages= kivy_utils.get_visible_page_heights(viewer=viewer)
	if not any([x['index'] == page.page_num for x in visible_pages]):
		return # bbox not on visible pages

	for x in visible_pages:
		if x['index'] != page.page_num:
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
def remove_box(*args):
	App.get_running_app().bubbBox.rectangle= (0,)*4