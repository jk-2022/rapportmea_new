from typing import Any, List, Optional
from flet import *

import sqlite3

# import json
from myaction import recuperer_liste_projets

from screens.projetscreen.projetupdateform import ProjetUpdateForm
# from uix.customdropdown import CustomDropDown

DB_PATH = "data/rapport.db"

class ProjetCard(Card):
    def __init__(self, page: Page, projet, formcontrol):
        super().__init__()
        self.expand=True
        self.elevation=1
        self.projet=projet
        self.formcontrol=formcontrol
        self.content=Container(
            on_click=lambda e: self.selectprojet(e),
            padding=padding.all(10),
            data=projet,
            ink=True,
            expand=True,
            content=Row(
                [
                    Container(
                        content=Column(
                            [
                                Text(f"{projet['create_at']}", size=11, italic=True),
                                Container(
                                    expand=True,
                                    content=Text(f"{projet['name']}", size=13, width=300)
                                    ),
                            ],
                        )
                        ),
                    Container(
                        width=60,
                        padding=padding.only(right=10),
                        expand=True,
                        content=Column(
                            [
                                IconButton(icon=Icons.EDIT, on_click=self.show_edit_projet),
                                IconButton(icon=Icons.DELETE, on_click=self.show_delete_projet),
                            ],
                            alignment=MainAxisAlignment.CENTER,
                        )
                    )
                ],alignment=MainAxisAlignment.SPACE_BETWEEN,
            )
        )
        
    def selectprojet(self,e):
        self.page.data['projet']=self.projet
        self.page.go("/rapport")


    def show_delete_projet(self,e):
        name=self.projet["name"]
        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("Nouveau projet"),
            content=Text(f"Voulez-vous supprimer {name} ?"),
            actions=[
                TextButton("Annuler", on_click=self.close_dlg),
                TextButton("Supprimer", on_click=self.del_projet),
            ],
            actions_alignment= MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.open(self.dlg_modal)
        self.page.update()
        
    def show_edit_projet(self,e):
        cont=ProjetUpdateForm(page=self.page,projet=self.projet,formcontrol=self)
        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("Modifier projet"),
            content=cont,
            actions=[
                TextButton("Annuler", on_click=self.close_dlg),
                TextButton("Modifier", on_click=cont.SaveData),
            ],
            actions_alignment= MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.open(self.dlg_modal)
        self.page.update()
        
    def close_dlg(self,e):
        self.page.close(self.dlg_modal)
        self.page.update()
        
    def del_projet(self,e):
        pid=int(self.projet['id'])
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM projets WHERE id=?", (pid,))
        conn.commit()
        conn.close()
        news_data= recuperer_liste_projets()
        self.page.data['projets']=news_data
        self.page.close(self.dlg_modal)
        self.formcontrol.load_projects()
        self.page.update()
        
    