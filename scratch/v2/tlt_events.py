from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color
from kivy.animation import Animation

from kivy_utils.classes.viewer import ImPage
import warnings, kivy_utils, numpy as np, functools

def get_box_fade():
	im_pg= ImPage()

	def to_color_dict(rgba): return dict(r=rgba[0], g=rgba[1], b=rgba[2], a=rgba[3])
	def to_focus(): return Animation(**to_color_dict(im_pg.focus_box_color), duration=im_pg.fade_time)
	def to_normal(): return Animation(**to_color_dict(im_pg.line_box_color), duration=im_pg.fade_time)

	anim= to_focus() + to_normal()
	for x in range(im_pg.fade_cycles-1):
		anim+= to_focus() + to_normal()

	return anim

def run_box_fade(box):
	Animation.stop_all(box.color)
	anim= get_box_fade()

	if box.hidden:
		box.show()
		def hide(*args): box.hide()
		anim.bind(on_complete=hide)

	anim.start(box.color)
	return

def run_text_fade(label):
	Animation.stop_all(label)

	def to_focus(): return Animation(color=label.focus_color, duration=label.fade_time)
	def to_normal(): return Animation(color=label.color, duration=label.fade_time)

	anim= to_focus() + to_normal()
	for x in range(label.fade_cycles-1):
		anim+= to_focus() + to_normal()

	orig= label.color
	def hide(*args): label.color= orig
	anim.bind(on_complete=hide)

	anim.start(label)


# move clicked row into view in viewer
def scroll_on_table_double_click(row, margin_ratio=0.1):
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
	target_scroll= 1 - target_y / scrollable_dist

	# if already in view, don't scroll
	if target_scroll <= app.viewer.scroll_y <= target_scroll + app.viewer.height / scrollable_dist:
		pass
	else: app.viewer.scroll_y= target_scroll

	highlight_on_focus(row)


# draw border around text in image when table row focused
def highlight_on_focus(row):
	app= App.get_running_app()

	for im_pg in app.viewer.im_pages:
		for box in im_pg.boxes: # grp is InstructionGroup
			if box.bubble is row.bubble:
				run_box_fade(box)
				run_text_fade(row.num)
				return

	return


# move clicked bubble into view in table
def scroll_on_bubble_double_click(line_box):
	app= App.get_running_app()

	# find row
	for row in app.tl_table.rows:
		if row.bubble is line_box.bubble:
			run_box_fade(line_box)
			run_text_fade(row.num)

			top_edge= row.pos[1]+row.height
			scrollable_dist= app.tl_table.layout.height - app.tl_table.height
			target_scroll= (top_edge - app.tl_table.height) / scrollable_dist

			# if already in view, don't scroll
			if target_scroll <= app.tl_table.scroll_y <= target_scroll + app.tl_table.height / scrollable_dist:
				pass
			else: app.tl_table.scroll_y= max(0,target_scroll)

			break
