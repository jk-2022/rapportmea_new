from flet import * 

class TraiText(Row):
    def __init__(self, title:str,bgcolor="white54",text_size=13, **k):
        super().__init__(**k)
        # alignment=MainAxisAlignment.CENTER,
        self.controls=[
            Container(height=2,expand=True,bgcolor=bgcolor),
            Text(f"{title}",size=text_size),
            Container(height=2,expand=True,bgcolor=bgcolor),
        ]