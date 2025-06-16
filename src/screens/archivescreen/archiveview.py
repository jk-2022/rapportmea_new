# projets_view.py
from flet import *
import os
from datetime import datetime

DB_PATH = "data/rapport.db"
ARCHIVES_PATH="generated_docs"


def get_exported_files():
    files = []
    if not os.path.exists(ARCHIVES_PATH):
        os.makedirs(ARCHIVES_PATH)
        return files

    for file_name in os.listdir(ARCHIVES_PATH):
        file_path = os.path.join(ARCHIVES_PATH, file_name)
        if os.path.isfile(file_path):
            ext = file_name.split(".")[-1].upper()
            created = datetime.fromtimestamp(os.path.getctime(file_path)).strftime("%d/%m/%Y %H:%M")
            files.append({"name": file_name, "type": ext, "date": created})
    return files

def get_icon_for_extension(extension: str):
    icons_map = {
        "pdf": Icons.PICTURE_AS_PDF,
        "docx": Icons.DESCRIPTION,
        "csv": Icons.TABLE_CHART,
        # Ajoute d'autres si besoin
    }
    return icons_map.get(extension, Icons.INSERT_DRIVE_FILE)

class ArchiveView(View):
    def __init__(self,page:Page):
        super().__init__()
        self.padding = 0
        self.page=page
        self.back_cnt = Container(
            content=Row(
                [IconButton(icon=Icons.CHEVRON_LEFT,on_click=self.page.on_view_pop)
                 ]
            )
        )
        self.archive_list = Column(
            expand=1
        )

        self.controls.append(SafeArea(
            Column(
                controls=[
                    Row(
                        controls=[
                            self.back_cnt,
                            Text('Archives')
                        ],
                        alignment=MainAxisAlignment.START
                    ),
                    Divider(),
                    self.archive_list
                        ]
                    ),expand=1
                )
            )
        self.load_archives()
        
    def load_archives(self):
        self.archive_list.controls.clear()
        for file in get_exported_files():
            icon = get_icon_for_extension(file["type"])
            row = ListTile(
                    leading=Icon(icon),
                    title=Text(f"{file['name']}"),
                    subtitle=Text(f"{file['date']}"),
                    trailing=IconButton(icon=Icons.DELETE, tooltip="Supprimer", on_click=lambda e, f=file: self.delete_file(f["name"])),
                    on_click=lambda e, f=file: os.startfile(os.path.join(ARCHIVES_PATH, f["name"])))
            self.archive_list.controls.append(row)

    def delete_file(self,file_name):
        os.remove(os.path.join(ARCHIVES_PATH, file_name))
        self.load_archives()
        self.page.update()
