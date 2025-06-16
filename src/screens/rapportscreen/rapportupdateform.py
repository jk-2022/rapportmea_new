from typing import Any, List, Optional
from flet import *

import sqlite3

from myaction import recuperer_liste_rapports

from uix.custominputfield import CustomInputField

class RapportUpdateForm(Container):
    def __init__(self, page: Page, rapport, formcontrol):
        super().__init__()
        self.padding = 0
        self.page=page
        self.width=450
        self.rapport=rapport
        self.projet=self.page.data['projet']
        self.formcontrol=formcontrol
        self.rapport_date = CustomInputField(title="Début ", width=300)
        self.rapport_date.value=str(rapport['rapport_date'])
        self.title_field = CustomInputField(title="Titre", width=300)
        self.title_field.value=rapport['title']
        self.content_field = TextField(label="Contenu", multiline=True, expand=True, height=100,value=rapport['content'])


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
        return {"rapport_date": rapport_date,"title": title_field, "content": content_field}


    def ConfirmeUpdate(self,e):
        self.page.close(self.formcontrol.dlg_modal)
        self.page.update()
        self.dialog = AlertDialog(
            title=Text("Confirmer modification"),
            content=Text("Voulez-vous enregistrer les modifications ?"),
            actions=[
                TextButton("Oui", on_click=self.UpdateData),
                TextButton("Annuler", on_click=lambda e: self.page.close(self.dialog))
                ],
            )
        self.page.open(self.dialog)
        self.update()
        
    def UpdateData(self, e):
        donnees = self.recupererDonnees()
        if not (donnees["title"] and donnees['content']):
            return
        conn = sqlite3.connect('data/rapport.db', check_same_thread=False)
        try:
            c = conn.cursor()
            c.execute("""
                    UPDATE rapports 
                     SET title = ?, content = ?, rapport_date = ? WHERE id = ?
                 """, (
                    donnees["title"], donnees["content"],
                    donnees["rapport_date"], self.rapport["rid"]
                ))
            conn.commit()
            list_rapports=recuperer_liste_rapports(self.projet['id'])
            self.page.data['rapports']=list_rapports
        except Exception as e:
            print(e)
            return False
        self.formcontrol.formcontrol.load_rapports()
        self.page.close(self.dialog)
        self.page.update()
