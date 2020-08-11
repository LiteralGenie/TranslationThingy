# -*- coding:utf8 -*-

from kivy.lang import Builder
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.core.window import Window
Window.size = (400, 700)

PLACEHOLDER_TEXT = u'''The bindings illustrated in tshirtman's example are created automatically when using kv-lang.
Notice how the "id: my_label" allows us to access the Label's attributes in the BoxLayout's height declaration.'''

kv_string = """
<Example>:
    orientation: 'vertical'
    BoxLayout:
        # colored background for affected area:
        canvas.before:
            Color:
                rgba: 0.3, .4, .4, .6
            Rectangle:
                pos: self.pos
                size: self.size
        size_hint_y: None
        height: my_label.height
        Label:
            id: my_label
            text: root.text
            font_size: '14dp'
            text_size: (self.width, None)
            size: self.texture_size
            valign: 'top'
            halign: 'left'
    BoxLayout:
        orientation: 'vertical'
        size_hint_y: 1
        canvas.before:
            Color:
                rgba: 0.9, .0, .5, .6
            Rectangle:
                pos: self.pos
                size: self.size
        TextInput:
            text: root.PLACEHOLDER_TEXT
            on_text: root.text = self.text
            text_size: self.size
            auto_indent: True
        Label:
            size_hint_y: None
            height: '50dp'
            text: 'String length: ' + str(len(root.text))
"""

Builder.load_string( kv_string )

class Example (BoxLayout ):
    PLACEHOLDER_TEXT = PLACEHOLDER_TEXT
    text = StringProperty(  )
    def __init__(self, **kwargs):
        super( Example, self).__init__(**kwargs)

class MyApp(App):
    def build(self):
        root = Example()
        return root

MyApp().run()