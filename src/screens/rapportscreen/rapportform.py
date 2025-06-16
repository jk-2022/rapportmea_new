from typing import Any, List, Optional
from flet import *

from datetime import date
import sqlite3

from myaction import recuperer_liste_projets, recuperer_liste_rapports

from uix.custominputfield import CustomInputField
from uix.traitext import TraiText

class RapportForm(Container):
    def __init__(self, page: Page, formcontrol):
        super().__init__()
        self.padding = 0
        self.page=page
        self.width=450
        self.projet=self.page.data['projet']
        self.formcontrol=formcontrol
        self.rapport_date = CustomInputField(title="Date ", width=300)
        self.rapport_date.value=str(date.today())
        self.title_field = CustomInputField(title="Titre", width=300)
        self.content_field = TextField(label="Contenu", multiline=True, height=100,expand=True)


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
                                self.rapport_date,
                            ]
                        ),
                        Row(
                            controls=[
                                self.title_field,
                            ]
                        ),
                        Row(
                            controls=[
                                self.content_field,
                            ]
                        ),
                    ]
                )
            )
        )

    def recupererDonnees(self):
        rapport_date = self.rapport_date.value
        title_field = self.title_field.value
        content_field = self.content_field.value
        return {"rapport_date": rapport_date, "title": title_field, "content": content_field}

    def SaveData(self, e):
        donnees = self.recupererDonnees()
        if not (donnees["title"] and donnees['content']):
            return
        conn = sqlite3.connect('data/rapport.db', check_same_thread=False)
        try:
            c = conn.cursor()
            c.execute("""
            INSERT INTO rapports (projet_id, title, content, rapport_date) 
            VALUES (?, ?, ?, ?)
            """, (self.projet['id'], donnees['title'], donnees['content'], donnees['rapport_date']))
            conn.commit()
            list_rapports=recuperer_liste_rapports(self.projet['id'])
            self.page.data['rapports']=list_rapports
        except Exception as e:
            print(e)
            return False
        self.formcontrol.load_rapports()
        self.formcontrol.close_dlg(e=None)

