from kivy.app import App
from kivy.lang.builder import Builder
from kivy.factory import Factory  # noqa

kv = """

ScreenManager:

"""


class Main(App):
    def build(self):
        self.mainkv = Builder.load_string(kv)
        return self.mainkv

    def on_start(self):
        self.show_screen("Home")
        return super().on_start()

    def show_screen(self, name, mode="forward"):
        self.load_string(name)

        if mode == "back":
            self.mainkv.transition.direction = "left"
        else:
            self.mainkv.transition.direction = "right"
        self.mainkv.transition.duration = 0.3
        self.mainkv.current = name

    def load_string(self, name):
        if not self.mainkv.has_screen(name):
            exec("from screens import %s" % name.lower())
            self.mainkv.add_widget(eval("Factory.%s()" % name))


Main().run()
