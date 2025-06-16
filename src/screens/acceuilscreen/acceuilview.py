from flet import *


class AcceuilView(View):
    def __init__(self,page:Page,**k):
        super().__init__()
        self.expand=True
        self.page=page
        appbar=Container(height=50,
                         content=Row(
                             [
                                Text("ACTIVITE ET RAPPORT ", text_align=TextAlign.CENTER, size=28, weight=FontWeight.BOLD)
                             ],alignment=MainAxisAlignment.CENTER
                         ))
        # text de banière================================
        
        self.controls.append(SafeArea(
            Column(
                controls=[
                    appbar,
                    Container(
                        content=Column(
                                    [
                                        ElevatedButton("Rapport d'activité", on_click=self.page_go_project),
                                        ElevatedButton("Liste d'ouvrages", on_click=self.page_go_list_ouvrage),
                                    ],
                                    expand=True,
                                    alignment=MainAxisAlignment.CENTER,
                                    spacing=40
                                ),
                            alignment=alignment.center,
                            expand=True
                            )
                        ],
                        expand=True
                    ),
            expand=True 
                )
            )

 
    def page_go_project(self,e):
        self.page.go('/project')
    
    def page_go_list_ouvrage(self,e):
        self.page.go('/list-ouvrage')