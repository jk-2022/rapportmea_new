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

        self.dropdown_type = DropdownM2(
        label="Type d’ouvrage",
        expand=True,
        options=[dropdown.Option("PMH"), dropdown.Option("PEA"), dropdown.Option("AEP")],
        on_change=lambda e: self.update_list()
        )

        self.dropdown_etat = DropdownM2(
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
                            IconButton(icon=Icons.CHEVRON_LEFT, on_click=self.page.on_view_pop),
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
                    # ElevatedButton("Générer PDF", on_click=self.generate_pdf),
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
            for ouvrage in ouvrages:
                des=['id','type_ouvrage', 'prefecture', 'commune', 'canton', 'localite', 'numero_irh', 'nombre',
                'lieu_implantation', 'type_energie', 'type_reservoir', 'volume_reservoir',
                'etat', 'cause_panne', 'observation','created_at']
                ouvrage=dict(zip(des, ouvrage))
                tb.rows.append(
                    DataRow(
                        cells=[DataCell(Row([
                            IconButton(icon="create", icon_color="blue",
                                        data=ouvrage,
                                        # on_click=self.showEdit
                                        ),
                            IconButton(icon=Icons.DELETE, icon_color="red",
                                        data=ouvrage["id"],
                                        # on_click=self.showDelete
                                        ),
                            ElevatedButton("articles", height=30,
                                            data=ouvrage,
                                            # on_click=self.goToLivScreen
                                            )
                        ]
                        )
                        ),
                            DataCell(Text(ouvrage["type_ouvrage"], color="white")),
                            DataCell(Text(ouvrage["prefecture"], color="white")),
                            DataCell(Text(ouvrage["commune"], color="white")),
                            DataCell(Text(ouvrage["canton"], color="white")),
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
            self.page.update()

    # def load_available_dates(self):
    #     """Charge toutes les dates disponibles dans la base pour ce projet"""
    #     conn = sqlite3.connect(DB_PATH)
    #     cursor = conn.cursor()
    #     cursor.execute(
    #         """
    #         SELECT DISTINCT rapport_date
    #         FROM rapports
    #         WHERE projet_id = ?
    #         ORDER BY rapport_date ASC
    #         """,
    #         (self.projet_id,)
    #     )
    #     dates = [row[0] for row in cursor.fetchall()]
    #     conn.close()

    #     if dates:
    #         self.start_date_dropdown.options = [dropdown.Option(date) for date in dates]
    #         self.end_date_dropdown.options = [dropdown.Option(date) for date in dates]
    #         self.page.update()

    # def filter_reports(self, e):
    #     self.report_list.controls.clear()
    #     start = self.start_date_dropdown.value
    #     end = self.end_date_dropdown.value

    #     if not start or not end:
    #         self.report_list.controls.append(Text("Veuillez choisir une date de début et de fin."))
    #         self.page.update()
    #         return

    #     # Vérification que la date de début est avant ou égale à la date de fin
    #     if start > end:
    #         self.report_list.controls.append(Text("⚠️ La date de début doit précéder la date de fin."))
    #         self.page.update()
    #         return

    #     conn = sqlite3.connect(DB_PATH)
    #     cursor = conn.cursor()
    #     cursor.execute(
    #         """
    #         SELECT title, content, rapport_date
    #         FROM rapports
    #         WHERE projet_id = ? AND rapport_date BETWEEN ? AND ?
    #         ORDER BY rapport_date DESC
    #         """,
    #         (self.projet_id, start, end)
    #     )
    #     reports = cursor.fetchall()
    #     conn.close()

    #     if not reports:
    #         self.report_list.controls.append(Text("Aucun rapport trouvé pour cette période."))
    #     else:
    #         for title, content, date in reports:
    #             self.report_list.controls.append(
    #                 Card(
    #                     content=Container(
    #                         content=Column([
    #                             Text(f"📅 {date}", weight="bold"),
    #                             Text(f"📝 {title}" ),
    #                             Text(content),
    #                         ]),
    #                         padding=10
    #                     )
    #                 )
    #             )
    #     self.page.update()
    
    # def generate_pdf(self, e):
    #     start = self.start_date_dropdown.value
    #     end = self.end_date_dropdown.value

    #     if not start or not end:
    #         self.dialog = AlertDialog(
    #             title=Text("⚠️ Choisir les deux dates.")
    #             )
    #         self.page.open(self.dialog)
    #         self.page.update()
    #         return

    #     conn = sqlite3.connect(DB_PATH)
    #     cursor = conn.cursor()
    #     cursor.execute(
    #         """
    #         SELECT rapport_date, title, content
    #         FROM rapports
    #         WHERE projet_id = ? AND rapport_date BETWEEN ? AND ?
    #         ORDER BY rapport_date ASC
    #         """,
    #         (self.projet_id, start, end)
    #     )
    #     reports = cursor.fetchall()
    #     conn.close()

    #     if not reports:
    #         self.dialog = AlertDialog(
    #             title=Text("Aucun rapport trouvé.")
    #             )
    #         self.page.open(self.dialog)
    #         self.page.update()
    #         return

    #     # Création du PDF
    #     pdf = FPDF()
    #     pdf.add_page()
    #     pdf.set_font("Arial", size=12)

    #     # Titre
    #     pdf.set_font("Arial", style="B", size=14)
    #     pdf.cell(200, 10, f"Rapports du {start} au {end}", ln=True, align="C")
    #     pdf.ln(10)

    #     # En-têtes du tableau
    #     pdf.set_font("Arial", style="B", size=12)
    #     pdf.cell(40, 10, "Date", 1)
    #     pdf.cell(50, 10, "Titre", 1)
    #     pdf.cell(100, 10, "Contenu", 1)
    #     pdf.ln()

    #     pdf.set_font("Arial", size=10)
    #     for report_date, title, content in reports:
    #         col_widths = [40, 50, 100]
    #         line_height = 6  # Hauteur de ligne standard
    #         x_start = pdf.get_x()
    #         y_start = pdf.get_y()

    #         # Calcule le nombre de lignes nécessaires pour chaque cellule
    #         content_lines = ceil(len(content) / 70)  # approx pour 100 de large
    #         title_lines = ceil(len(title) / 35)      # approx pour 50 de large
    #         max_lines = max(content_lines, title_lines, 1)
    #         row_height = max_lines * line_height

    #         # --- Cellule DATE ---
    #         pdf.set_xy(x_start, y_start)
    #         pdf.multi_cell(col_widths[0], row_height, report_date, border=1)

    #         # --- Cellule TITRE ---
    #         pdf.set_xy(x_start + col_widths[0], y_start)
    #         pdf.multi_cell(col_widths[1], row_height, title, border=1)

    #         # --- Cellule CONTENU (avec saut automatique sur plusieurs lignes) ---
    #         pdf.set_xy(x_start + col_widths[0] + col_widths[1], y_start)
    #         current_y = pdf.get_y()
    #         current_x = pdf.get_x()

    #         # Enregistre la position initiale
    #         lines = content.split('\n')
    #         wrapped = [content[i:i+90] for i in range(0, len(content), 90)]

    #         for line in wrapped:
    #             pdf.multi_cell(col_widths[2], line_height, line, border=0)
    #         end_y = pdf.get_y()

    #         # Dessiner bordure autour du contenu manuellement
    #         pdf.rect(current_x, current_y, col_widths[2], row_height)

    #         # Position suivante : à gauche + plus bas
    #         pdf.set_xy(x_start, y_start + row_height)

    #     # Dossier documents
    #     output_dir = "generated_docs"
    #     os.makedirs(output_dir, exist_ok=True)
    #     filename = f"{output_dir}/rapport_{start}_to_{end}.pdf"
    #     pdf.output(filename)


    #     self.page.open(SnackBar(Text(f"✅ PDF généré avec succès : {filename}")))
    #     self.page.update()

