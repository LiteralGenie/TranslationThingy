import kivy

from kivy.config import Config
kivy.require('1.11.1')
Config.set('kivy', 'log_level', 'debug')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color, Line

import kivy_utils as kutils
import utils.endic_utils as endic
import utils.papago_utils as translator

class OcrReader(App):
    def __init__(self, dir, chapNum=None):
        self.chapDir= dir
        self.title= "FionaBestGirl"
        self.chapNum= chapNum
        super().__init__()

    def build(self):
        self.root= GridLayout(cols=2)

        self.addLeft()
        self.addRight()
        self.initShit()

        return self.root

    def addLeft(self, name=None):
        # self.viewer= kutils.Viewer()
        self.viewer= kutils.Viewer().build(globDir=self.chapDir, chapNum=self.chapNum)
        self.root.add_widget(self.viewer)

    def addRight(self):
        self.rLabels= [Label(text=f"Label {x}", font_name='C:/Programming/KnightRunReader/data/fonts/NotoSansKR-Regular.otf')
                       for x in range(6)]

        for i in [1,3,5]:
            self.rLabels[i].size_hint_x= None
            self.rLabels[i].width= 400
        self.rLabels[4].halign= "left"
        self.rLabels[5].width= 0
        self.rLabels[5].text= ""


        rCol= GridLayout(rows=3, cols=2)
        for x in self.rLabels: rCol.add_widget(x)
        self.root.add_widget(rCol)

    def initShit(self):
        Window.bind( mouse_pos= kutils.wait(onMouse, delay=0.1, root=self) )
        self.viewer.fbind('on_scroll_stop', onScroll, root=self)

        with self.viewer.canvas:
            Color(0,0,1,0.5)
            self.wordBox= Line(size=(30,30), width=1.25)
            Color(1,0,0,0.3)
            self.lineBox= Line(size=(110,110), width=1.25, dash_length=0.5, dash_offest=1)

def onMouse(window, pos, root=None):
    processWord(window, pos, root=root)
    debug(window, pos, root=root)

def onScroll(window, pos, root=None):
    # root.wordBox.size= root.lineBox.size= (0,0) # Rectangle
    root.wordBox.rectangle= root.lineBox.rectangle= (0,)*4

def processWord(window, pos, root=None):
    r= root.viewer

    abs_y= kutils.get_y_abs_top(pos[1], r.scroll_y, r.im_heights)
    pageNum= kutils.getPageNum(abs_y, r.im_heights)
    pg_y= kutils.get_y_pg_top(abs_y, pageNum, r.im_heights)

    word,line,wbb,lbb= kutils.getWordLine(pos[0], pg_y, r.ocr_data[pageNum])

    if word and line:
        root.wordBox= kutils.modBox(root.wordBox, wbb, pg_y, pos[1])
        root.lineBox= kutils.modBox(root.lineBox, lbb, pg_y, pos[1])

        line_tl= translator.getTranslation(line, delay=3)
        showInfo(word, line, line_tl, root.rLabels)

def showInfo(word, line, mtl, labels):
    dictInfo= endic.search(word)

    meanings= [x['meaning'] for x in dictInfo['meanings']]
    meanings= [f"{i}) " + x for i,x in enumerate(meanings)]
    meanings= ',\n'.join(meanings)

    phrases= []
    for i,x in enumerate(dictInfo['phrases']):
        h= f"({x['hanja']})" if x['hanja'] else ''
        t= f"{i}) " + x['phrase'] + h + "\t---\t[" + " / ".join(x['meanings'])[:60] + "]"
        phrases.append(t)
    phrases= ',\n'.join(phrases)

    labels[0].text= f"Word:\t\"{word}\""
    labels[0].text+= f"\n\nLine:\t\"{line}\""
    labels[0].text+= f"\n\nMTL:\t\"{mtl}\""

    labels[2].text= f"Meanings of {word}:\n{div}\n{meanings}"
    labels[4].text= f"Phrases:\n{div}\n{phrases}"

div= '-'.join(['']*20)
def debug(window, pos, root=None):
    scroll_y= root.viewer.scroll_y
    heights= root.viewer.im_heights
    rLabels= root.rLabels

    abs_y= kutils.get_y_abs_top(pos[1], scroll_y, heights)
    pageNum= kutils.getPageNum(abs_y, heights)
    pg_y= kutils.get_y_pg_top(abs_y, pageNum, heights)

    boop= ""
    text= f"Current Position:"
    text+= f"\n{div}"
    text+= f"\n{boop}scroll=({round(scroll_y,4)})"
    text+= f"\n{boop}(rel_bl)   x={int(pos[0])}   y={int(pos[1])}"
    text+= f"\n{boop}(abs_tl)   x={int(pos[0])}   y={int(abs_y)}"
    text+= f"\n{boop}(rel_pg)   x={int(pos[0])}   y={int(pg_y)}"

    text+= f"\n\nPage {pageNum+1}"

    rLabels[3].text= text

if __name__ == '__main__':
    chapNum= 209
    chapDir= rf"C:\scans\Knight Run\{chapNum}/*.png"

    kutils.doFullScreen()
    OcrReader(dir=chapDir, chapNum=chapNum).run()