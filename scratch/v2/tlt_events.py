from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color
from kivy.animation import Animation

from kivy_utils.classes.viewer import ImPage
import warnings, kivy_utils, numpy as np, functools

def to_color_dict(rgba):
	return dict(r=rgba[0], g=rgba[1], b=rgba[2], a=rgba[3])

def get_fade_animation(im_pg):
	def to_focus(): return Animation(**to_color_dict(im_pg.focus_box_color), duration=im_pg.fade_time)
	def to_normal(): return Animation(**to_color_dict(im_pg.line_box_color), duration=im_pg.fade_time)

	anim= to_focus() + to_normal()
	for x in range(im_pg.fade_cycles-1):
		anim+= to_focus() + to_normal()

	return anim

# move clicked row into view
def scroll_on_table_double_click(row, margin_ratio=0.1, padding=None):
	app= App.get_running_app()

	page= row.page
	bubble= row.bubble
	if page is None or bubble is None: return

	tmp= page.page_num
	target_y= sum(app.viewer.im_heights[:tmp-1])
	target_y+= bubble.bbox['y'] + int(bubble.bbox['h']/2)

	scrollable_dist= sum(app.viewer.im_heights) - app.viewer.height

	target_y-= margin_ratio * app.viewer.height # padding
	target_y= max(0, target_y)
	target_scroll= target_y / scrollable_dist

	app.viewer.scroll_y= 1-target_scroll
	highlight_on_focus(row, padding=padding)


# draw border around text in image when table row focused
def highlight_on_focus(row, padding=None):
	app= App.get_running_app()

	for im_pg in app.viewer.im_pages:
		for box in im_pg.boxes: # grp is InstructionGroup
			if box.bubble is row.bubble:
				Animation.stop_all(box.color)
				anim= get_fade_animation(im_pg)

				if box.hidden:
					box.show()
					def hide(*args): box.hide()
					anim.bind(on_complete=hide)

				anim.start(box.color)
				return

	return



# remove highlight on scroll
def unfocus(*args):
	App.get_running_app().bubbBox.rectangle= (0,)*4