from utils import kivy_utils
from classes.app import App


# chap_num can be any identifier but glob_dir should refer to an actual set of images
chap_num= 165
glob_dir= rf"C:\scans\Knight Run\{chap_num}/*.png"

kivy_utils.doFullScreen()
app= App(glob_dir=glob_dir, chap_num=chap_num, mtl=True)
app.run()