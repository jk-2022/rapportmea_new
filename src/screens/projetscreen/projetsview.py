# projets_view.py
from flet import *
import sqlite3
import os

from screens.projetscreen.projetcard import ProjetCard
from screens.projetscreen.projetform import ProjetForm

DB_PATH = "data/rapport.db"

class ProjectView(View):
    def __init__(self,page:Page):
        super().__init__()
        self.padding = 0
        self.page=page
        self.project_list = Column(
            expand=1
        )
        self.floating_action_button = FloatingActionButton(icon=Icons.ADD, on_click=self.show_projet)

        self.controls.append(SafeArea(
            Column(
                controls=[
                    Container(
                        content=Row(
                                [
                                IconButton(icon=Icons.ARROW_BACK, on_click=self.page.on_view_pop),
                                Text("Liste des projets ", text_align=TextAlign.CENTER)
                                ]
                                # ,alignment=MainAxisAlignment.CENTER
                            ),
                            # alignment=alignment.center,
                    ),
                    Divider(),
                    self.project_list
                        ]
                    )
                )
            )
        self.load_projects()
        
    def show_projet(self,e):
        projet_content = ProjetForm(self.page, self)
        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("Nouveau projet"),
            content=projet_content,
            actions=[
                TextButton("Annuler", on_click=self.close_dlg),
                TextButton("Enregistrer", on_click=projet_content.SaveData),
            ],
            actions_alignment= MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.open(self.dlg_modal)
        self.page.update()
        
    def load_projects(self):
        self.project_list.controls.clear()
        projets=self.page.data['projets']
        if projets:
            for projet in projets:
                des=['id','name','create_at']
                projet=dict(zip(des, projet))
                self.project_list.controls.append(
                ProjetCard(page=self.page, projet=projet,formcontrol=self)
            )

    def add_project(self, e):
        name = self.project_input.value.strip()
        if not name:
            return
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO projects (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()
        self.project_input.value = ""
        self.load_projects()
        
    def close_dlg(self, e):
        self.page.close(self.dlg_modal)
        self.page.update()
