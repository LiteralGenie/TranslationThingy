from kivy.config import Config
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.uix.image import AsyncImage
from kivy.uix.textinput import TextInput

Config.set('kivy', 'log_level', 'debug')

from kivy.graphics import Color, Line
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.recycleview import RecycleView

from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.graphics.opengl_utils import gl_register_get_size
import cv2

kv = """
<Test>: # BoxLayout
    layout: layout
    
    RecycleView:
        height: 1000
        BoxLayout:
            id: layout
            orientation: "vertical"
            size_hint_y: None
            height: 1000
            
<Label>:
    height: 100            
"""
Builder.load_string(kv)

class Test(BoxLayout):
    layout= ObjectProperty()

    def populate(self, num=2):
        for i in range(1,num+1):
            # label= Label(text=f"Label {i}")
            label= AsyncImage(source=r"C:\Users\Anne\PycharmProjects\KRR/gralb.png")

            with label.canvas:
                Color(1,0,0, 1)
                Line(points=[100*i,200*i, 300*i,400*i], width=5)
            self.layout.add_widget(label)

        return self

class TestApp(App):
    def build(self):
        self.root= Test().populate(num=5)
        return self.root

if __name__ == '__main__':
    TestApp().run()