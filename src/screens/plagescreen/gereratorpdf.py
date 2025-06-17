from fpdf import FPDF
from fpdf.enums import XPos, YPos

class GeneratorPDF(FPDF):
    def __init__(self,rappor_title):
        super().__init__()
        self.rappor_title=rappor_title

    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, f"{self.rappor_title}", border=False, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.ln(5)

    def table_row(self,report, col_widths):
        # Sauvegarde de la position actuelle
        x, y = self.get_x(), self.get_y()

        # Calcule la hauteur du contenu (plus long)
        contenu_lines = self.multi_cell(col_widths[2], self.font_size + 2, report['content'], dry_run=True, output="LINES")
        row_height = len(contenu_lines) * (self.font_size + 2)

        # DATE
        self.set_xy(x, y)
        self.multi_cell(col_widths[0], row_height, report['rapport_date'], border=1, align='L')
        
        # TITRE
        self.set_xy(x + col_widths[0], y)
        self.multi_cell(col_widths[1], row_height, report['title'], border=1, align='L')

        # CONTENU
        self.set_xy(x + col_widths[0] + col_widths[1], y)
        self.multi_cell(col_widths[2], self.font_size + 2, report['content'], border=1, align='L')

        # Repositionne le curseur à gauche pour la ligne suivante
        self.set_y(y + row_height)

        # Repositionne le curseur pour la prochaine ligne
        # self.ln()

    def get_string_height(self, width, text):
        """Calcule la hauteur que prendra le texte dans une cellule de largeur donnée."""
        lines = self.multi_cell(width, self.font_size + 2, text, border=0, align='L', dry_run=True, output="LINES"
        )
        return len(lines) * (self.font_size + 2)


# Exemple de données
donnees = [
    ("2025-06-01", "Bilan quotidien", "Voici un résumé très long qui devrait être affiché dans une cellule multi-ligne correctement, sans être tronqué ni dépasser de la cellule."),
    ("2025-06-02", "Analyse", "Court contenu."),
]

# Création du PDF
# pdf = PAGEPDF()
# pdf.set_auto_page_break(auto=True, margin=15)
# pdf.add_page()
# pdf.set_font("Arial", size=12)

# # Largeurs des colonnes
# col_widths = [30, 40, 120]

# # En-têtes du tableau
# headers = ["Date", "Titre", "Contenu"]
# for i in range(len(headers)):
#     pdf.cell(col_widths[i], 10, headers[i], border=1, align="C")
# pdf.ln()

# # Données
# for date, titre, contenu in donnees:
#     pdf.table_row(date, titre, contenu, col_widths)

# # Sauvegarde du PDF
# pdf.output("rapport.pdf")
