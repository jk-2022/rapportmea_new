from typing import Any, List, Optional
from flet import *

import sqlite3

# import json
from myaction import recuperer_liste_projets

from uix.custominputfield import CustomInputField

class ProjetUpdateForm(Container):
    def __init__(self, page: Page, projet, formcontrol):
        super().__init__()
        self.padding = 0
        self.page=page
        self.width=450
        self.projet=projet
        self.formcontrol=formcontrol
        self.date = Text(f"{projet['create_at']}")
        self.name = CustomInputField(title="Nom projet", height=40)
        self.name.value=projet["name"]


        self.content = Card(
            elevation=20,
            content=Container(
                padding=15,
                expand=True,
                content=Column(
                    scroll="always",
                    spacing=10,
                    controls=[
                        Row(
                            controls=[
                                self.date
                            ]
                        ),
                        Row(
                            controls=[
                                self.name,
                            ]
                        ),
                    ]
                )
            )
        )


    def recupererDonnees(self):
        name = self.name.value
        date = self.date.value
        return {"name": name, "created_at": date}
        
    def SaveData(self, e):
        donnees = self.recupererDonnees()
        pid=self.projet['id']
        print(donnees)
        conn = sqlite3.connect('data/rapport.db', check_same_thread=False)
        try:
            c = conn.cursor()
            c.execute("UPDATE projets SET name=? WHERE id=?", (donnees["name"], pid))
            conn.commit()
            list_projet=recuperer_liste_projets()
            self.page.data['projets']=list_projet
        except Exception as e:
            print(e)
            return False
        self.formcontrol.formcontrol.load_projects()
        self.formcontrol.close_dlg(e=None)
        
    # def save_edit(ev):
    #     new_name = name_input.value.strip()
    #     if new_name:
    #         conn = sqlite3.connect(DB_PATH)
    #         cursor = conn.cursor()
    #         cursor.execute("UPDATE projects SET name=? WHERE id=?", (new_name, pid))
    #         conn.commit()
    #         conn.close()
    #         self.load_projects()


