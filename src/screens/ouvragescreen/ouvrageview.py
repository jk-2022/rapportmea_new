
# projets_view.py
from flet import *
import sqlite3
import os

from myaction import recuperer_liste_ouvrages
from screens.ouvragescreen.ouvragecard import OuvrageCard
from screens.ouvragescreen.ouvrageform import OuvrageForm


DB_PATH = "data/rapport.db"

class OuvrageView(View):
    def __init__(self,page:Page):
        super().__init__()
        self.padding = 0
        self.page=page
        self.ouvrage_list = Column(
            expand=1,
            scroll=ScrollMode.ALWAYS
        )
        self.searsh_button = ElevatedButton("filter",icon=Icons.SEARCH, on_click=self.go_filter_page)
        self.add_button = ElevatedButton("ajouter ouvrage",icon=Icons.ADD, on_click=self.show_projet)

        self.controls.append(SafeArea(
            Column(
                controls=[
                    Container(
                        content=Row(
                                [
                                IconButton(icon=Icons.ARROW_BACK, on_click=self.page.on_view_pop),
                                Text("Tous ouvrages confondus ", text_align=TextAlign.CENTER)
                                ]
                                # ,alignment=MainAxisAlignment.CENTER
                            )
                    ),
                    Divider(),
                    Container(
                        content=Row(
                            [
                                self.searsh_button,
                                self.add_button
                            ],alignment=MainAxisAlignment.SPACE_BETWEEN
                        ),
                        padding=padding.only(left=10, right=10)
                    ),
                    self.ouvrage_list
                        ]
                    )
                )
            )
        self.load_ouvrages()
        
    def show_projet(self,e):
        projet_content = OuvrageForm(self.page, self)
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
        
    def load_ouvrages(self):
        self.ouvrage_list.controls.clear()
        ouvrages=recuperer_liste_ouvrages()
        # print(ouvrages)
        if ouvrages:
            for ouvrage in ouvrages:
                des=['id','type_ouvrage', 'prefecture', 'commune', 'canton', 'localite', 'numero_irh', 'nombre',
                'lieu_implantation', 'type_energie', 'type_reservoir', 'volume_reservoir',
                'etat', 'cause_panne', 'observation','created_at']
                ouvrage=dict(zip(des, ouvrage))
                self.ouvrage_list.controls.append(
                OuvrageCard(page=self.page, ouvrage=ouvrage,formcontrol=self)
            )
        self.page.update()

    # def add_project(self, e):
    #     name = self.project_input.value.strip()
    #     if not name:
    #         return
    #     conn = sqlite3.connect(DB_PATH)
    #     cursor = conn.cursor()
    #     cursor.execute("INSERT INTO projects (name) VALUES (?)", (name,))
    #     conn.commit()
    #     conn.close()
    #     self.project_input.value = ""
    #     self.load_ouvrages()

    def go_filter_page(self,e):
        self.page.go("/filtrer-ouvrage")
        
    def close_dlg(self, e):
        self.page.close(self.dlg_modal)
        self.page.update()
