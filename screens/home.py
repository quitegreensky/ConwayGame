from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from classes.main_layout import MainLayout
from classes.dialog import ModalBox

Builder.load_string(
    """

<Home>:
    name: "Home"
    canvas.before:
        Color:
            rgba: 1,1,1,0.4
        RoundedRectangle:
            pos: self.pos
            size: self.size

    MainLayout:
        size_hint: None,None
        size: app.root.size
""")


class Home(Screen):
    
    def on_enter(self, *args):
        dialog = ModalBox()
        dialog.open()
        return super().on_enter(*args)