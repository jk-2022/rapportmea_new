# weekly_report_view.py
import sqlite3
from flet import *

from screens.rapportouvragescreen.customtitlelabel import CustomTitleLabel
from screens.rapportouvragescreen.ouvrageupdateform import OuvrageUpdateForm


DB_PATH = "data/rapport.db"

class RapportOuvrageView(View):
    def __init__(self, page : Page):
        super().__init__()
        self.page=page
        self.ouvrage=self.page.data['ouvrage']
        self.ouvrage_id = self.ouvrage['id']
        self.ouvrage_type = self.ouvrage['type_ouvrage']
        
        self.cnt_labs=Column(
            expand=True,
            scroll=ScrollMode.ALWAYS
        )
        self.report_content = Card(
            elevation=5,
            expand=True,
            content=self.cnt_labs
            
        )
        self.controls.append(
            SafeArea(
                Column(
                    controls=[
                        Row(
                            [
                            IconButton(icon=Icons.ARROW_BACK,on_click=self.page.on_view_pop),
                            Text(f"📁 ouvrage : {self.ouvrage_type}")
                            ]
                        ),
                        Divider(),
                        self.report_content,
                        Row([
                            ElevatedButton("Modifier", on_click=self.show_edit_ouvrage),
                            ElevatedButton("Supprimer", on_click=self.show_delete_ouvrage),
                            ]
                            )
                    ]
                ),expand=1
            )
        )
        self.load_rapports()
        
    def load_rapports(self):
        self.cnt_labs.controls.clear()
        rapports=self.page.data['ouvrage']
        print(rapports)
        if rapports:
            for key,value in rapports.items():
                self.cnt_labs.controls.append(
                    CustomTitleLabel(title=key,value=value)
                )
        self.page.update()
                

    def show_edit_ouvrage(self,e):
        cont=OuvrageUpdateForm(page=self.page,ouvrage=self.ouvrage, formcontrol=self)
        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("Modifier ouvrage"),
            content=cont,
            actions=[
                TextButton("Annuler", on_click=self.close_dlg),
                TextButton("Modifier", on_click=cont.ConfirmeUpdate),
            ],
            actions_alignment= MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.open(self.dlg_modal)
        self.page.update()

    def goPlage(self,e):
        self.page.go("/plage")

    def show_delete_ouvrage(self,e):
        title=self.ouvrage['numero_irh']
        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("Confirmation"),
            content=Text(f"Voulez-vous supprimer {title} ?"),
            actions=[
                TextButton("Non", on_click=self.close_dlg),
                TextButton("Oui", on_click=self.del_ouvrage),
            ],
            actions_alignment= MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.open(self.dlg_modal)
        self.page.update()

    def del_ouvrage(self,e):
        rid=int(self.ouvrage['id'])
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ouvrages WHERE id=?", (rid,))
        conn.commit()
        conn.close()
        self.page.close(self.dlg_modal)
        self.page.on_view_pop(e=None)
    
    def close_dlg(self, e):
        self.page.close(self.dlg_modal)
        self.page.update()
