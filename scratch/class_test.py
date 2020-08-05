from kivy.config import Config
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.uix.image import AsyncImage
from kivy.uix.textinput import TextInput

Config.set('kivy', 'log_level', 'debug')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.graphics.opengl_utils import gl_register_get_size
import cv2

kv = """
<Test>: # BoxLayout
    layout: layout
    
    ScrollView:
        size_hint: (1,1)
        smooth_scroll_end: 500
        
        
        BoxLayout:
            id: layout
            orientation: "horizontal"
            size_hint: (None,None)
"""
Builder.load_string(kv)

class Test(BoxLayout):
    layout= ObjectProperty()

    def populate(self, num=2):
        im_path= "C:/Users/Anne/PycharmProjects/KRR/gralb2.png"

        for i in range(num):
            im_dims= tuple(reversed(cv2.imread(im_path).shape[:2]))
            im= AsyncImage(
                source=im_path,
                size_hint=(None, None),
                size=im_dims
            )
            self.layout.add_widget(im)

            if self.layout.orientation == "vertical":
                self.layout.height+= im_dims[1]
                self.layout.width= im_dims[0]
            else:
                self.layout.width+= im_dims[0]
                self.layout.height= im_dims[1]

        return self

class TestApp(App):
    def build(self):
        self.root= Test().populate(num=500)
        return self.root

if __name__ == '__main__':
    TestApp().run()