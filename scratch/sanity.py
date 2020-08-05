from kivymd.app import MDApp
from kivy.lang import Builder
from threading import Thread
from time import sleep
from kivy.clock import mainthread


KV = '''
Screen:

    MDProgressBar:
        id: progress_bar
        pos_hint: {'center_x': .5, 'center_y': .5}
        size_hint_x: .7
        value: 0
        color: [0,0,0,1]

    MDRaisedButton:
        text: 'Run'
        pos_hint: {'center_x': .5, 'center_y': .1}
        on_release: app.do_things()
    '''


class TestApp(MDApp):

    def build(self):
        self.number = 0
        return Builder.load_string(KV)

    @mainthread
    def update_progress_bar(self):
        self.root.ids.progress_bar.value += 10

    def loop(self):
        for self.number in range(1, 11):
            print(self.number)
            self.update_progress_bar()
            sleep(2)

    def do_things(self):
        t1 = Thread(target=self.loop, daemon=True)
        t1.start()


if __name__ == "__main__":
    app = TestApp()
    app.run()