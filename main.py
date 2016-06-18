from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.codeinput import CodeInput
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen

from pygments.styles.borland import BorlandStyle
from pygments.lexers.python import Python3Lexer

Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '1100')
Config.set('graphics', 'height', '800')


def _create_screen(content, name):
    def switch_screen(screen_manager): screen_manager.current = screen_manager.next()

    screen = Screen(name=name)
    layout = BoxLayout(orientation='vertical')

    swap_button = Button(text='Swap Screen')
    swap_button.bind(on_release=lambda _: switch_screen(screen.manager))
    swap_button.size_hint = (1.0, 0.1)

    layout.add_widget(swap_button)
    layout.add_widget(content)
    screen.add_widget(layout)

    return screen


class TestApp(App):
    def build(self):
        code = "import datetime\nprint datetime.now().strftime('%Y-%m-%d %H:%M:%S')"
        parent_layout = ScreenManager()

        editor_layout = BoxLayout(orientation='horizontal')
        layout1 = BoxLayout(orientation='vertical')
        layout1.add_widget(Label(text='Input'))
        layout1.add_widget(Label(text='Output'))
        editor_layout.add_widget(layout1)
        editor_layout.add_widget(CodeInput(text=code, lexer=Python3Lexer(), style=BorlandStyle))

        job_layout = BoxLayout(orientation='horizontal')
        job_layout.add_widget(Label(text='TODO'))

        parent_layout.add_widget(_create_screen(editor_layout, 'editor'))
        parent_layout.add_widget(_create_screen(job_layout, 'Jobs'))

        return parent_layout

TestApp().run()

