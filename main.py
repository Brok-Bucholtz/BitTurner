from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.codeinput import CodeInput
from kivy.config import Config

from pygments.styles.borland import BorlandStyle
from pygments.lexers.python import Python3Lexer

Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '1100')
Config.set('graphics', 'height', '800')


class TestApp(App):
    def build(self):
        code = "import datetime\nprint datetime.now().strftime('%Y-%m-%d %H:%M:%S')"

        parent_layout = PageLayout()
        page_1 = BoxLayout(orientation='horizontal')
        parent_layout.add_widget(page_1)
        page_2 = BoxLayout(orientation='horizontal')
        parent_layout.add_widget(page_2)

        layout1 = BoxLayout(orientation='vertical')
        layout1.add_widget(Label(text='Input'))
        layout1.add_widget(Label(text='Output'))
        page_1.add_widget(layout1)

        page_1.add_widget(CodeInput(text=code, lexer=Python3Lexer(), style=BorlandStyle))\

        return parent_layout

TestApp().run()

