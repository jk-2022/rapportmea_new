 # main.py
from flet import *
from screens.screens import *
from myaction import create_table_projet, create_table_rapport, recuperer_liste_projets, get_exported_files,creer_table_ouvrages

def fetch_data():
    projets=recuperer_liste_projets()
    return {'projets':projets}

def main(page: Page):
    page.title = "Gestion des projets"
    page.scroll = True
    page.window.width=450
    page.theme_mode = ThemeMode.DARK
    theme = Theme()
    theme.page_transitions.android = PageTransitionsTheme.android
    get_exported_files()
    create_table_projet()
    create_table_rapport()
    creer_table_ouvrages()
    page.data= fetch_data()
    
    def route_change(route):
        if page.route == "/":
            page.views.append(AcceuilView(page))
        elif page.route == "/project":
            page.views.append(ProjectView(page))
        elif page.route == "/rapport":
            page.views.append(RapportView(page))
        elif page.route == "/plage":
            page.views.append(PlageView(page))
        elif page.route == "/archive":
            page.views.append(ArchiveView(page))
        elif page.route == "/list-ouvrage":
            page.views.append(OuvrageView(page))
        elif page.route == "/rapport-ouvrage":
            page.views.append(RapportOuvrageView(page))
        elif page.route == "/filtrer-ouvrage":
            page.views.append(FiltreOuvrageView(page))
        page.update()

    def on_view_pop(e: ViewPopEvent):
        # 🔙 Cette fonction est appelée quand l'utilisateur appuie sur le bouton retour Android
        print(page.views)
        if len(page.views) > 1:
            page.views.pop()
            page.go(page.views[-1].route)
        else:
            # Si on est sur la première page, quitter l'app
            page.window.close()

    
    page.views.append(AcceuilView(page))
    page.on_route_change = lambda e: route_change(page)
    page.on_view_pop = lambda e: on_view_pop(page)
    page.update()

app(target=main)
