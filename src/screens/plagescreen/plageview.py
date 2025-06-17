from flet import *
import sqlite3
import os

DB_PATH = "data/rapport.db"

from .gereratorpdf import GeneratorPDF
from .generatordocx import GeneratorDOCX
class PlageView(View):
    def __init__(self, page):
        super().__init__(route="/")
        self.page = page
        self.projet=self.page.data["projet"]
        self.projet_id = self.projet["id"]
        self.repports_list=[]

        self.start_date_dropdown = Dropdown(label="Date début",expand=True)
        self.end_date_dropdown = Dropdown(label="Date fin",expand=True)

        self.back_cnt = Container(
            content=Row(
                [IconButton(icon=Icons.CHEVRON_LEFT, on_click=self.page.on_view_pop)
                 ]
            )
        )

        self.report_list = Column(
            expand=1,
            scroll=ScrollMode.ALWAYS
        )

        self.controls.append(
            SafeArea(
                Column(
                    [
                    Row(
                        [
                        self.back_cnt,
                        Text("Filtrer les rapports par période")
                        ]
                    ),
                    Container(
                        # expand=True,
                        content=Row(
                            [
                            self.start_date_dropdown,
                            self.end_date_dropdown,
                            ],
                            alignment=MainAxisAlignment.SPACE_AROUND
                        )
                    ),
                    ElevatedButton("Afficher les rapports", on_click=self.filter_reports),
                    Divider(),
                    self.report_list,
                    Row(
                        [
                            ElevatedButton("Générer PDF", on_click=self.generate_pdf),
                            ElevatedButton("Générer DOCX", on_click=self.generate_docx),
                        ],alignment=MainAxisAlignment.SPACE_EVENLY
                    )
                    ]
                ), expand=True
            )
        )

        self.load_available_dates()

    def load_available_dates(self):
        """Charge toutes les dates disponibles dans la base pour ce projet"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT DISTINCT rapport_date
            FROM rapports
            WHERE projet_id = ?
            ORDER BY rapport_date ASC
            """,
            (self.projet_id,)
        )
        dates = [row[0] for row in cursor.fetchall()]
        conn.close()

        if dates:
            self.start_date_dropdown.options = [dropdown.Option(date) for date in dates]
            self.end_date_dropdown.options = [dropdown.Option(date) for date in dates]
            self.page.update()

    def filter_reports(self, e):
        self.report_list.controls.clear()
        start = self.start_date_dropdown.value
        end = self.end_date_dropdown.value

        if not start or not end:
            self.report_list.controls.append(Text("Veuillez choisir une date de début et de fin."))
            self.page.update()
            return

        # Vérification que la date de début est avant ou égale à la date de fin
        if start > end:
            self.report_list.controls.append(Text("⚠️ La date de début doit précéder la date de fin."))
            self.page.update()
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT title, content, rapport_date
            FROM rapports
            WHERE projet_id = ? AND rapport_date BETWEEN ? AND ?
            ORDER BY rapport_date DESC
            """,
            (self.projet_id, start, end)
        )
        reports = cursor.fetchall()
        conn.close()
        # print(reports)
        des=["title", "content", "rapport_date"]
        if reports:
            for report in reports:
                rep=dict(zip(des, report))
                self.repports_list.append(rep)

        if not reports:
            self.report_list.controls.append(Text("Aucun rapport trouvé pour cette période."))
        else:
            for title, content, date in reports:
                self.report_list.controls.append(
                    Card(
                        content=Container(
                            content=Column([
                                Text(f"📅 {date}", weight="bold"),
                                Text(f"📝 {title}" ),
                                Row([
                                    Text(content, weight=FontWeight.W_100, size=12, theme_style=TextThemeStyle.BODY_MEDIUM)
                                ]),
                            ]),
                            padding=10
                        )
                    )
                )
        self.page.update()

    def generate_docx(self, e):
        start = self.start_date_dropdown.value
        end = self.end_date_dropdown.value
        reports=self.repports_list
        print(reports)
        if not reports:
            self.dialog = AlertDialog(
                title=Text("Aucun rapport trouvé.")
                )
            self.page.open(self.dialog)
            self.page.update()
            return

        # Sauvegarde du PDF
        output_dir = "generated_docs"
        rapport_title=f"Rapports du {start} au {end}"
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{output_dir}/{rapport_title}.docx"

        # Création du DOCX
        docx = GeneratorDOCX(donnees=reports,titre=rapport_title,filename=filename)
        docx.create_docx()


        self.page.open(SnackBar(Text(f"✅ PDF généré avec succès : {filename}")))
        self.page.update()
    
    def generate_pdf(self, e):
        start = self.start_date_dropdown.value
        end = self.end_date_dropdown.value
        reports=self.repports_list
        if not reports:
            self.dialog = AlertDialog(
                title=Text("Aucun rapport trouvé.")
                )
            self.page.open(self.dialog)
            self.page.update()
            return

        # Création du PDF
        rapport_title=f"Rapports du {start} au {end}"
        pdf = GeneratorPDF(rappor_title=rapport_title)
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)

        # Largeurs des colonnes
        col_widths = [30, 40, 120]

        # En-têtes du tableau
        headers = ["Date", "Titre", "Activités"]
        for i in range(len(headers)):
            pdf.cell(col_widths[i], 10, headers[i], border=1, align="C")
        pdf.ln()

        # Données
        for report in reports:
            pdf.table_row(report, col_widths)

        # Sauvegarde du PDF
        output_dir = "generated_docs"
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{output_dir}/{rapport_title}.pdf"
        pdf.output(filename)


        self.page.open(SnackBar(Text(f"✅ PDF généré avec succès : {filename}")))
        self.page.update()

