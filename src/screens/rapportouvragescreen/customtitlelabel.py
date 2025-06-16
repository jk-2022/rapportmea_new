from flet import *

class CustomTitleLabel(Container):
    def __init__(self,title,value,**kwargs):
        super().__init__()
        self.padding=10
        self.content=Row(
            [
                Container(
                    content=Text(title, weight=FontWeight.BOLD,height=20),
                    width=150,
                    alignment=alignment.center_left
                ),
                Container(
                    content=Text(':'),
                    width=20,
                    alignment=alignment.center_left
                ),
                Container(
                    content=Text(value),
                    expand=True,
                    alignment=alignment.center_right
                )
            ],spacing=0
        )