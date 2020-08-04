from kivy.uix.textinput import TextInput

# Bugfix for focus_previous not working: https://github.com/kivy/kivy/issues/6560
class TxtInput(TextInput):
	def keyboard_on_key_down(self, window, keycode, text, modifiers):
		from kivy.base import EventLoop
		from kivy.clock import Clock
		import sys
		_is_osx = sys.platform == 'darwin'

		# Keycodes on OS X:
		ctrl, cmd = 64, 1024
		key, key_str = keycode
		win = EventLoop.window

		# This allows *either* ctrl *or* cmd, but not both.
		modifiers = set(modifiers) - {'capslock', 'numlock'}
		is_shortcut = (modifiers == {'ctrl'} or (
			_is_osx and modifiers == {'meta'}))
		is_interesting_key = key in (list(self.interesting_keys.keys()) + [27])

		modifiers= list(modifiers) # genie fix
		if not self.write_tab and super(TextInput,
			self).keyboard_on_key_down(window, keycode, text, modifiers):
			return True

		if not self._editable:
			# duplicated but faster testing for non-editable keys
			if text and not is_interesting_key:
				if is_shortcut and key == ord('c'):
					self.copy()
			elif key == 27:
				self.focus = False
			return True

		if text and not is_interesting_key:

			self._hide_handles(win)
			self._hide_cut_copy_paste(win)
			win.remove_widget(self._handle_middle)

			# check for command modes
			# we use \x01INFO\x02 to get info from IME on mobiles
			# pygame seems to pass \x01 as the unicode for ctrl+a
			# checking for modifiers ensures conflict resolution.

			first_char = ord(text[0])
			if not modifiers and first_char == 1:
				self._command_mode = True
				self._command = ''
			if not modifiers and first_char == 2:
				self._command_mode = False
				self._command = self._command[1:]

			if self._command_mode:
				self._command += text
				return

			_command = self._command
			if _command and first_char == 2:
				from_undo = True
				_command, data = _command.split(':')
				self._command = ''
				if self._selection:
					self.delete_selection()
				if _command == 'DEL':
					count = int(data)
					if not count:
						self.delete_selection(from_undo=True)
					end = self.cursor_index()
					self._selection_from = max(end - count, 0)
					self._selection_to = end
					self._selection = True
					self.delete_selection(from_undo=True)
					return
				elif _command == 'INSERT':
					self.insert_text(data, from_undo)
				elif _command == 'INSERTN':
					from_undo = False
					self.insert_text(data, from_undo)
				elif _command == 'SELWORD':
					self.dispatch('on_double_tap')
				elif _command == 'SEL':
					if data == '0':
						Clock.schedule_once(lambda dt: self.cancel_selection())
				elif _command == 'CURCOL':
					self.cursor = int(data), self.cursor_row
				return

			if is_shortcut:
				if key == ord('x'):  # cut selection
					self._cut(self.selection_text)
				elif key == ord('c'):  # copy selection
					self.copy()
				elif key == ord('v'):  # paste clipboard content
					self.paste()
				elif key == ord('a'):  # select all
					self.select_all()
				elif key == ord('z'):  # undo
					self.do_undo()
				elif key == ord('r'):  # redo
					self.do_redo()
			else:
				is_sdl2 = (EventLoop.window.__class__.__module__ ==
						   'kivy.core.window.window_sdl2')
				if is_sdl2:
					# we expect to get managed key input via on_textinput
					return
				if self._selection:
					self.delete_selection()
				self.insert_text(text)
			# self._recalc_size()
			return

		if is_interesting_key:
			self._hide_cut_copy_paste(win)
			self._hide_handles(win)

		if key == 27:  # escape
			self.focus = False
			return True
		elif key == 9:  # tab
			self.insert_text(u'\t')
			return True

		k = self.interesting_keys.get(key)
		if k:
			key = (None, None, k, 1)
			self._key_down(key)