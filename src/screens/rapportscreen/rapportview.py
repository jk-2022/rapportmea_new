# weekly_report_view.py
from flet import *

from screens.rapportscreen.rapportcard import RapportCard
from screens.rapportscreen.rapportform import RapportForm

from myaction import recuperer_liste_rapports

DB_PATH = "data/rapport.db"

class RapportView(View):
    def __init__(self, page : Page):
        super().__init__()
        self.page=page
        self.projet=self.page.data['projet']
        self.project_id = self.projet['id']
        self.project_name = self.projet['name']
        self.back_cnt = Container(
            content=Row(
                [IconButton(icon=Icons.ARROW_BACK,on_click=self.page.on_view_pop)
                 ]
            )
        )
        self.report_list = Column(
                    expand=1,
                    scroll=ScrollMode.ALWAYS,
                    )

        self.controls.append(
            SafeArea(
                Column(
                    controls=[
                        Row(
                            [
                            self.back_cnt,
                            Text(f"📁 Projet : {self.project_name}")
                            ]
                        ),
                        Row([
                            ElevatedButton("Ajouter un rapport", on_click=self.show_add_rappord),
                            ElevatedButton("Choix plage de rapport", on_click=self.goPlage),
                            ElevatedButton("archives", on_click=self.goArchive),
                            ]
                            ),
                        Divider(),
                        Text("📋 Rapports journalier :"),
                        self.report_list
                    ]
                ),expand=1
            )
        )
        self.load_rapports()
        
    def load_rapports(self):
        self.report_list.controls.clear()
        rapports=recuperer_liste_rapports(self.projet["id"])
        if rapports:
            for rapport in rapports:
                des=['rid', 'title', 'content', 'rapport_date', 'created_at']
                rapport=dict(zip(des, rapport))
                self.report_list.controls.append(
                    RapportCard(page=self.page,rapport=rapport,formcontrol=self)
                )
      
        self.page.update()
        
    def show_add_rappord(self,e):
        rapport_content = RapportForm(self.page, self)
        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("Nouveau projet"),
            content=rapport_content,
            actions=[
                TextButton("Annuler", on_click=self.close_dlg),
                TextButton("Enregistrer", on_click=rapport_content.SaveData),
            ],
            actions_alignment= MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.open(self.dlg_modal)
        self.page.update()

    def goPlage(self,e):
        self.page.go("/plage")

    def goArchive(self,e):
        self.page.go("/archive")
    
    def close_dlg(self, e):
        self.page.close(self.dlg_modal)
        self.page.update()
