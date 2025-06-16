from flet import *

PRIMARY = "teal"


class CustomInputField(TextField):
    def __init__(self, title: str, width = None, height = None, password: bool = False, read_only: bool = False, on_change=None,value=''):
        super().__init__()
        self.height=height
        self.border_color="#bbbbbb"
        self.expand=True
        self.hint_text=title
        self.border_width=0.6
        self.cursor_height=12
        self.cursor_width=1
        self.cursor_color="white"
        self.color="white"
        self.width=width
        self.content_padding=padding.only(left=5, right=5)
        self.text_size=11
        self.value=value
        self.read_only=read_only
        self.on_change=on_change
        self.on_focus=lambda e: self.focus_shadow(e)
        self.on_blur=lambda e: self.blur_shadow(e)
        self.password=password


    def focus_shadow(self, e):
        self.border_color = PRIMARY
        self.update()

    def blur_shadow(self, e):
        self.border_color = "#bbbbbb"
        self.update()


