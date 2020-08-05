import time, threading
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivymd.app import MDApp

KV = '''
Screen:

    BoxLayout:
        orientation:'vertical'
        cols: 3
        spacing: 30
        padding: 30

        MDProgressBar:
            id: progress_bar
            value: 0
            color: [0,0,0,1]

        Button:
            text: 'Run'
            on_release: app.do_things()
            
        TextInput:
    '''

class TestApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(KV)
        self.number = 1
        self.previous_loop_number = 0

    def build(self):
        return self.screen

    def update_progress(self):
        def tmp(dt): # check for update
            print("found",self.number)
            if self.screen.ids.progress_bar.value < 100:
                self.screen.ids.progress_bar.value= self.number*10
            else: print("cancelling"); event.cancel()
        event= Clock.schedule_interval(tmp, 1)

    def loop(self):
        def tmp(dt): # trigger update
            print("updating")
            if self.number < 10:
                self.number+= 1
            else: print("cancelling"); event.cancel()
        event= Clock.schedule_interval(tmp, 1)

    def do_things(self):
        t1 = threading.Thread(target=self.loop)
        t2 = threading.Thread(target=self.update_progress)
        t1.start()
        t2.start()
        t1.join()
        t2.join()


if __name__ == "__main__":
    TestApp().run()