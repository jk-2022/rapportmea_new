import sqlite3
from flet import *
from myaction import recuperer_liste_ouvrages

from uix.custominputfield import CustomInputField

class OuvrageForm(Container):
    def __init__(self, page: Page, formcontrol):
        super().__init__()
        self.padding = 0
        self.page=page
        self.width=450
        self.formcontrol=formcontrol
        # dateTime = datetime.now().strftime("%d/%m/%Y")
        self.type_ouvrage = Dropdown(label="Type d'ouvrage", options=[
        dropdown.Option("PMH"), dropdown.Option("PEA"), dropdown.Option("AEP")
        ])

        self.prefecture = CustomInputField(title="Préfecture")
        self.commune = CustomInputField(title="Commune")
        self.canton = CustomInputField(title="Canton")
        self.localite = CustomInputField(title="Localité")
        self.numero_irh = CustomInputField(title="N° IRH")
        self.nombre = CustomInputField(title="Nombre")
        self.lieu = CustomInputField(title="Lieu d'implantation")
        self.type_energie = CustomInputField(title="Type d'énergie")
        self.type_reservoir = CustomInputField(title="Type de réservoir")
        self.volume = CustomInputField(title="Volume du réservoir")

        self.etat = Dropdown(label="État de l'ouvrage", options=[
            dropdown.Option("Bon état"),
            dropdown.Option("En panne"),
            dropdown.Option("Abandonné")
        ])
        self.cause = TextField(label="Cause de la panne (si applicable)")
        self.observation = TextField(label="Observation")



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
                        self.nombre, self.lieu, self.type_energie, self.type_reservoir, self.volume,
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
            "volume_reservoir": self.volume.value or 0,
            "etat": self.etat.value,
            "cause_panne": self.cause.value,
            "observation": self.observation.value
        }
        return data

    def SaveData(self, e):
        data = self.recupererDonnees()
        print(data)
        conn = sqlite3.connect('data/rapport.db', check_same_thread=False)
        try:
            c = conn.cursor()
            c.execute('''
                INSERT INTO ouvrages (
                    type_ouvrage, prefecture, commune, canton, localite, numero_irh, nombre,
                    lieu_implantation, type_energie, type_reservoir, volume_reservoir,
                    etat, cause_panne, observation
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data["type_ouvrage"], data["prefecture"], data["commune"], data["canton"],
                data["localite"], data["numero_irh"], data["nombre"], data["lieu_implantation"],
                data["type_energie"], data["type_reservoir"], data["volume_reservoir"],
                data["etat"], data["cause_panne"], data["observation"]
            ))
            conn.commit()
            conn.close()
            list_ouvrage=recuperer_liste_ouvrages()
            self.page.data['ouvrages']=list_ouvrage
        except Exception as e:
            print(e)
            return False
        self.formcontrol.load_ouvrages()
        self.formcontrol.close_dlg(e=None)




