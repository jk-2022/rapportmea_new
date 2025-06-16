import sqlite3
from flet import *
from myaction import recuperer_one_ouvrages

from uix.custominputfield import CustomInputField

class OuvrageUpdateForm(Container):
    def __init__(self, page: Page, ouvrage, formcontrol):
        super().__init__()
        self.padding = 0
        self.page=page
        self.width=450
        self.formcontrol=formcontrol
        self.ouvrage=ouvrage
        self.type_ouvrage = Dropdown(label="Type d'ouvrage", options=[
        dropdown.Option("PMH"), dropdown.Option("PEA"), dropdown.Option("AEP")
        ],value=self.ouvrage['type_ouvrage']
        )

        self.prefecture = CustomInputField(title="Préfecture",value=self.ouvrage['prefecture'])
        self.commune = CustomInputField(title="Commune",value=self.ouvrage['commune'])
        self.canton = CustomInputField(title="Canton",value=self.ouvrage['canton'])
        self.localite = CustomInputField(title="Localité",value=self.ouvrage['localite'])
        self.numero_irh = CustomInputField(title="N° IRH",value=self.ouvrage['numero_irh'])
        self.nombre = CustomInputField(title="Nombre",value=self.ouvrage['nombre'])
        self.lieu = CustomInputField(title="Lieu d'implantation",value=self.ouvrage['lieu_implantation'])
        self.type_energie = CustomInputField(title="Type d'énergie",value=self.ouvrage['type_energie'])
        self.type_reservoir = CustomInputField(title="Type de réservoir",value=self.ouvrage['type_reservoir'])
        self.volume_reservoir = CustomInputField(title="Volume du réservoir",value=self.ouvrage['volume_reservoir'])

        self.etat = Dropdown(label="État de l'ouvrage", options=[
            dropdown.Option("Bon état"),
            dropdown.Option("En panne"),
            dropdown.Option("Abandonné")
        ],value=self.ouvrage['etat'])
        
        self.cause = TextField(label="Cause de la panne (si applicable)",value=self.ouvrage['cause_panne'])
        self.observation = TextField(label="Observation",value=self.ouvrage['observation'])



        self.content = Card(
            elevation=20,
            content=Container(
                padding=15,
                expand=True,
                content=Column(
                    scroll="always",
                    spacing=10,
                    controls=[
                        self.type_ouvrage, self.prefecture, self.commune, self.canton, self.localite, self.numero_irh,
                        self.nombre, self.lieu, self.type_energie, self.type_reservoir, self.volume_reservoir,
                        self.etat, self.cause, self.observation,
                            ]
                        )
                    )
                )

    def recupererDonnees(self):
        data = {
            "type_ouvrage": self.type_ouvrage.value,
            "prefecture": self.prefecture.value,
            "commune": self.commune.value,
            "canton": self.canton.value,
            "localite": self.localite.value,
            "numero_irh": self.numero_irh.value,
            "nombre": self.nombre.value or 0,
            "lieu_implantation": self.lieu.value,
            "type_energie": self.type_energie.value,
            "type_reservoir": self.type_reservoir.value,
            "volume_reservoir": self.volume_reservoir.value or 0,
            "etat": self.etat.value,
            "cause_panne": self.cause.value,
            "observation": self.observation.value
        }
        return data
    
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
        data = self.recupererDonnees()
        conn = sqlite3.connect('data/rapport.db', check_same_thread=False)
        try:
            c = conn.cursor()
            c.execute('''
                UPDATE  ouvrages SET
                    type_ouvrage=?, prefecture=?, commune=?, canton=?, localite=?, numero_irh=?, nombre=?,
                    lieu_implantation=?, type_energie=?, type_reservoir=?, volume_reservoir=?,
                    etat=?, cause_panne=?, observation=? WHERE id=? ''', (
                data["type_ouvrage"], data["prefecture"], data["commune"], data["canton"],
                data["localite"], data["numero_irh"], data["nombre"], data["lieu_implantation"],
                data["type_energie"], data["type_reservoir"], data["volume_reservoir"],
                data["etat"], data["cause_panne"], data["observation"], self.ouvrage["id"]
            ))
            conn.commit()
            conn.close()
            data['id']=self.ouvrage["id"]
            ouvrage=recuperer_one_ouvrages(int(data['id']))
            self.page.data['ouvrage']=ouvrage
        except Exception as e:
            return False
        self.formcontrol.load_rapports()
        self.page.close(self.dialog)
        self.page.update()




