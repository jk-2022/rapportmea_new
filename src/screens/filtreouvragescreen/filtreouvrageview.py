import csv
from flet import *
import sqlite3
from fpdf import FPDF
import os
from math import ceil

from .datatable import Mytable, tb

DB_PATH = "data/rapport.db"

class FiltreOuvrageView(View):
    def __init__(self, page:Page):
        super().__init__(route="/")
        self.page = page

        self.liste_ouvrage_filtrer=[]
        self.dropdown_type = Dropdown(
        label="Type",
        expand=True,
        options=[dropdown.Option("PMH"), dropdown.Option("PEA"), dropdown.Option("AEP")],
        on_change=lambda e: self.update_list()
        )

        self.dropdown_etat = Dropdown(
            label="État",
            expand=True,
            options=[dropdown.Option("Bon état"), dropdown.Option("En panne"), dropdown.Option("Abandonné")],
            on_change=lambda e: self.update_list()
        )

        self.dropdown_prefecture = TextField(
            label="Préfecture", on_change=lambda e: self.update_list(),
            expand=True,
        )

        self.ouvrage_column_list = Column(
            expand=1,
            scroll=ScrollMode.ALWAYS
        )

        self.controls.append(
            SafeArea(
                Column(
                    [
                        Row(
                            [
                            IconButton(icon=Icons.ARROW_BACK, on_click=self.page.on_view_pop),
                            Text("Filtrer les ouvrages"),
                            ]
                        ),
                    Container(
                        # expand=True,
                        content=Row(
                            [
                            self.dropdown_type,
                            self.dropdown_etat,
                            self.dropdown_prefecture
                            ],
                            alignment=MainAxisAlignment.SPACE_AROUND
                        )
                    ),
                    Divider(),
                    Mytable,
                    ElevatedButton("Générer PDF", on_click=self.showGenerate_pdf),
                    ]
                ), expand=True
            )
        )



    def get_filtered_ouvrages(self,type_ouvrage=None, etat=None, prefecture=None):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        query = "SELECT * FROM ouvrages WHERE 1=1"
        params = []

        if type_ouvrage:
            query += " AND type_ouvrage = ?"
            params.append(type_ouvrage)
        if etat:
            query += " AND etat = ?"
            params.append(etat)
        if prefecture:
            query += " AND prefecture = ?"
            params.append(prefecture)

        cursor.execute(query, params)
        ouvrages = cursor.fetchall()
        conn.close()
        return ouvrages
    
    def update_list(self):
        self.ouvrage_column_list.controls.clear()
        ouvrages = self.get_filtered_ouvrages(
            type_ouvrage=self.dropdown_type.value,
            etat=self.dropdown_etat.value,
            prefecture=self.dropdown_prefecture.value
        )

        if ouvrages:
            tb.rows = []
            self.liste_ouvrage_filtrer=[]
            for ouvrage in ouvrages:
                self.liste_ouvrage_filtrer.append(list(ouvrage))
                des=["id","type_ouvrage", "prefecture", "commune", "canton", "localite", "numero_irh", "nombre",
                "lieu_implantation", "type_energie", "type_reservoir", "volume_reservoir",
                "etat", "cause_panne", "observation","created_at"]
                ouvrage=dict(zip(des, ouvrage))
                tb.rows.append(
                    DataRow(
                        cells=[
                            DataCell(Text(ouvrage["type_ouvrage"], color="white")),
                            DataCell(Text(ouvrage["prefecture"], color="white")),
                            DataCell(Text(ouvrage["commune"], color="white")),
                            DataCell(Text(ouvrage["canton"], color="white")),
                            DataCell(Text(ouvrage["localite"], color="white")),
                            DataCell(Text(ouvrage["numero_irh"], color="white")),
                            DataCell(Text(ouvrage["nombre"], color="white")),
                            DataCell(Text(ouvrage["lieu_implantation"], color="white")),
                            DataCell(Text(ouvrage["type_energie"], color="white")),
                            DataCell(Text(ouvrage["type_reservoir"], color="white")),
                            DataCell(Text(ouvrage["volume_reservoir"], color="white")),
                            DataCell(Text(ouvrage["etat"], color="white")),
                            DataCell(Text(ouvrage["cause_panne"], color="white")),
                            DataCell(Text(ouvrage["observation"], color="white")),
                            DataCell(Text(ouvrage["created_at"], color="white")),
                        ]
                    )
                )
            tb.update()
        else:
            tb.rows=[]
        self.page.update()

    def showGenerate_pdf(self,e):
        titlefield=TextField(expand=True, height=40)
        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("Nom du fichier"),
            content=titlefield,
            actions=[
                TextButton("Annuler", on_click=self.close_dlg),
                TextButton("Exporter", on_click = lambda e : self.generate_csv(titlefield.value)),
            ],
            actions_alignment= MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        self.page.open(self.dlg_modal)
        self.page.update()

    def generate_csv(self, filename):
        row=self.liste_ouvrage_filtrer
        if row:
            with open(f"generated_docs/{filename}.csv", mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file, delimiter=";")
                writer.writerow(["id","type_ouvrage", "prefecture", "commune", "canton", "localite", "numero_irh", "nombre",
                "lieu_implantation", "type_energie", "type_reservoir", "volume_reservoir",
                "etat", "cause_panne", "observation","created_at"])
                for r in row:
                    writer.writerow(r)
            self.page.open(SnackBar(Text(f"{filename} saved successfuly"),open=True))
            self.close_dlg(e=None)
            return True
        self.page.open(SnackBar(Text(f"Error for vaving {filename}"),open=True))
    
    def close_dlg(self,e):
        self.page.close(self.dlg_modal)
        self.page.update()
            
