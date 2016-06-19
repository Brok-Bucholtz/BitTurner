from types import FunctionType
from io import StringIO

import sys
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.codeinput import CodeInput
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.stacklayout import StackLayout

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


def _run_sandbox(code, input):
    def sandbox():
        # noinspection PyUnresolvedReferences
        exec(exec_code)

    codeOut = StringIO()
    codeErr = StringIO()
    sys.stdout = codeOut
    sys.stderr = codeErr

    scope = {'__builtins__': __builtins__, 'exec_code':code, 'input': input}
    sandboxed = FunctionType(sandbox.__code__, scope)
    try:
        sandboxed()  # will throw NameError, builtins is not defined
    except Exception as exception:
        outputs = None
        errors = exception
    else:
        errors = codeErr.getvalue()
        outputs = codeOut.getvalue()

    # restore stdout and stderr
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    codeOut.close()
    codeErr.close()

    return outputs, errors


def build_main_ui():
    def _update_code_output(code, inputs, output_widgets):
        for input, output_widget in zip(inputs, output_widgets):
            output, error = _run_sandbox(code, input)
            output_display = output if not error else error
            output_widget.text = 'Code Output: {}'.format(output_display)

    start_inputs = [1, 2, 3, 4]
    start_outputs = [2, 3, 4, 5]
    start_code = "print(input)"

    parent_layout = ScreenManager()
    editor_layout = BoxLayout(orientation='horizontal')
    score_layout = BoxLayout(orientation='vertical')
    output_layout = StackLayout()
    code_output_widgets = []

    list_box_properties = {
        'size_hint': (1.0, None),
        'height': 30}

    code_input = CodeInput(text=start_code, lexer=Python3Lexer(), style=BorlandStyle)

    run_code_button = Button(text='Run Code', size_hint=(1.0, 0.1))
    run_code_button.bind(on_release=lambda _: _update_code_output(code_input.text, start_inputs, code_output_widgets))

    for input, expected_output in zip(start_inputs, start_outputs):
        code_output_widget = Label(text='<ERROR>', **list_box_properties)
        code_output_widgets.append(code_output_widget)
        output_layout.add_widget(
            Label(text='Input: {}  Output: {}'.format(input, expected_output), **list_box_properties))
        output_layout.add_widget(code_output_widget)
    _update_code_output(code_input.text, start_inputs, code_output_widgets)

    score_layout.add_widget(run_code_button)
    score_layout.add_widget(Label(text='Code Goal', size_hint=(1.0, 0.1)))
    score_layout.add_widget(output_layout)
    score_layout.size_hint = (0.3, 1.0)
    editor_layout.add_widget(score_layout)
    editor_layout.add_widget(code_input)

    job_layout = BoxLayout(orientation='horizontal')
    job_layout.add_widget(Label(text='TODO'))

    parent_layout.add_widget(_create_screen(editor_layout, 'editor'))
    parent_layout.add_widget(_create_screen(job_layout, 'Jobs'))

    return parent_layout
