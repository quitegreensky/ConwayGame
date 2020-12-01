from kivy.lang.builder import Builder
from kivy.uix.modalview import ModalView
from kivy.properties import StringProperty


Builder.load_string(
    """
<ModalBox>
    size_hint: 0.8,0.8
    padding: dp(10)
    ScrollView:
        canvas.before:
            Color:
                rgba: 1,1,1,1
            RoundedRectangle:
                pos: self.pos
                size: self.size
        Label:
            padding: (dp(10),dp(10))
            text: root.text
            color: 0,0,0,1
            size_hint_y: None
            text_size: self.width, None 
            height: self.texture_size[1]          
            halign: "left"
            valign: "top"
            markup:True
    """)


class ModalBox(ModalView):
    text = StringProperty("""
[b][size=20]- Conway's Game of Life [/size][/b]\n
The Game of Life, also known simply as Life, is a cellular automaton devised by \
the British mathematician John Horton Conway in 1970.It is a zero-player game, \
meaning that its evolution is determined by its initial state, \
requiring no further input. One interacts with the Game of Life by creating \
an initial configuration and observing how it evolves. It is Turing complete and \
can simulate a universal constructor or any other Turing machine.\n
[b]Rules[/b]\n
1- Any live cell with two or three live neighbours survives.\n
2- Any dead cell with three live neighbours becomes a live cell.\n
3- All other live cells die in the next generation. Similarly, all other dead cells stay dead.\n
[b]How to play?[/b]\n
Simply draw your initial configuration and let it go! \
Double tap to reset everything.
    """)
