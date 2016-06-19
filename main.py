from kivy.app import App

from ui.main import build_main_ui


class MainApp(App):
    def build(self):
        return build_main_ui()

MainApp().run()

