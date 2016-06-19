import sys
from io import StringIO
from types import FunctionType

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.codeinput import CodeInput
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout
from pygments.lexers.python import Python3Lexer
from pygments.styles.borland import BorlandStyle


def _run_sandbox(code, input):
    def sandbox():
        # noinspection PyUnresolvedReferences
        exec(exec_code)

    code_out = StringIO()
    code_error = StringIO()
    sys.stdout = code_out
    sys.stderr = code_error

    scope = {'__builtins__': __builtins__, 'exec_code': code, 'input': input}
    sandboxed = FunctionType(sandbox.__code__, scope)
    try:
        sandboxed()  # will throw NameError, builtins is not defined
    except Exception as exception:
        outputs = None
        errors = exception
    else:
        errors = code_error.getvalue()
        outputs = code_out.getvalue()

    # restore stdout and stderr
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    code_out.close()
    code_error.close()

    return outputs, errors


def _update_code_output(code, inputs, output_widgets):
    for input, output_widget in zip(inputs, output_widgets):
        output, error = _run_sandbox(code, input)
        output_display = output if not error else error
        output_widget.text = 'Code Output: {}'.format(output_display)


def get_editor_layout(start_code, start_inputs, start_outputs):
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

    return editor_layout
