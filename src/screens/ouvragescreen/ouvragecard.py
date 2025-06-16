# from typing import Any, List, Optional
from flet import *

# from datetime import datetime
import sqlite3

# import json
from myaction import recuperer_liste_ouvrages

# from screens.projetscreen.projetupdateform import ProjetUpdateForm
# from uix.customdropdown import CustomDropDown

DB_PATH = "data/rapport.db"

class OuvrageCard(Card):
    def __init__(self, page: Page, ouvrage, formcontrol):
        super().__init__()
        self.expand=True
        self.elevation=1
        self.ouvrage=ouvrage
        self.formcontrol=formcontrol
        self.content=Container(
            on_click=lambda e: self.selectouvrage(e),
            padding=padding.all(10),
            data=ouvrage,
            ink=True,
            expand=True,
            content=Row(
                [
                    Container(
                        content=Column(
                            [
                                Text(f"{ouvrage['created_at']}", size=11, italic=True),
                                Container(
                                    expand=True,
                                    content=Column(
                                        [
                                            Row(
                                                [
                                                    Text(f"{ouvrage['type_ouvrage']} / {ouvrage['numero_irh']}", size=13, width=300),
                                                ]
                                            ),
                                            Row(
                                                [
                                                    Text(f"{ouvrage['lieu_implantation']}/ {ouvrage['localite']} / {ouvrage['prefecture']}", size=13, width=300),
                                                ]
                                            ),
                                            Row(
                                                [
                                                    Text(f"{ouvrage['etat']}", size=13, width=300)
                                                ]
                                            )
                                        ],spacing=2
                                    )
                                    ),
                            ],
                        )
                        ),
                    
                    ],alignment=MainAxisAlignment.SPACE_BETWEEN,
                )
            
            )
        
    def selectouvrage(self,e):
        self.page.data['ouvrage']=self.ouvrage
        self.page.go("/rapport-ouvrage")


    def show_delete_ouvrage(self,e):
        numero_irh=self.ouvrage["numero_irh"]
        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("Suppression"),
            content=Text(f"Voulez-vous supprimer {numero_irh} ?"),
            actions=[
                TextButton("Annuler", on_click=self.close_dlg),
                TextButton("Supprimer", on_click=self.del_ouvrage),
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
        
    def del_ouvrage(self,e):
        pid=int(self.ouvrage['id'])
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ouvrages WHERE id=?", (pid,))
        conn.commit()
        conn.close()
        news_data= recuperer_liste_ouvrages()
        self.page.data['ouvrages']=news_data
        self.page.close(self.dlg_modal)
        self.formcontrol.load_ouvrages()
        self.page.update()
        
    