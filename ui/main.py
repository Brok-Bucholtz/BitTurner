from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen

from ui.editor import get_editor_layout

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


def build_main_ui():
    start_inputs = [1, 2, 3, 4]
    start_outputs = [2, 3, 4, 5]
    start_code = "print(input)"

    parent_layout = ScreenManager()
    editor_layout = get_editor_layout(start_code, start_inputs, start_outputs)
    job_layout = BoxLayout(orientation='horizontal')
    job_layout.add_widget(Label(text='TODO'))
    parent_layout.add_widget(_create_screen(editor_layout, 'editor'))
    parent_layout.add_widget(_create_screen(job_layout, 'Jobs'))

    return parent_layout
