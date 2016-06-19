from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


def get_job_layout():
    job_layout = BoxLayout(orientation='horizontal')
    job_layout.add_widget(Label(text='TODO'))

    return job_layout
