from typing import Any, List, Optional
from flet import *

from datetime import datetime
import sqlite3

# import json
from myaction import recuperer_liste_projets

from uix.custominputfield import CustomInputField
from uix.traitext import TraiText
# from uix.customdropdown import CustomDropDown

class ProjetForm(Container):
    def __init__(self, page: Page, formcontrol):
        super().__init__()
        self.padding = 0
        self.page=page
        self.width=450
        self.formcontrol=formcontrol
        dateTime = datetime.now().strftime("%d/%m/%Y")
        self.date = Text(f"{dateTime}", height=40)
        self.name = CustomInputField(title="Nom projet", height=40)
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
        conn = sqlite3.connect('data/rapport.db', check_same_thread=False)
        try:
            c = conn.cursor()
            c.execute("""
                        INSERT INTO projets(name,created_at) VALUES(?,?)
                        """, (donnees["name"],  donnees["created_at"]))
            conn.commit()
            list_projet=recuperer_liste_projets()
            self.page.data['projets']=list_projet
        except Exception as e:
            print(e)
            return False
        self.formcontrol.load_projects()
        self.formcontrol.close_dlg(e=None)
