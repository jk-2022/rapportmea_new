from flet import *

tb = DataTable(
    columns=[
        # DataColumn(Text("Actions", color="white",
        #            weight="bold", text_align=TextAlign.CENTER, size=12)),
        DataColumn(Text("Type", color="white",weight="bold", text_align=TextAlign.CENTER, size=12)),
        DataColumn(Text("Prefecture", color="white", weight="bold", size=12)),
        DataColumn(Text("Commune", color="white", weight="bold", size=12)),
        DataColumn(Text("Canton", color="white", weight="bold", size=12)),
        DataColumn(Text("Localite", color="white",weight="bold", text_align=TextAlign.CENTER, size=12)),
        DataColumn(Text("N° Irh", color="white",weight="bold", size=12)),
        DataColumn(Text("Nombre", color="white", weight="bold", size=12)),
        DataColumn(Text("Lieu", color="white", weight="bold", size=12)),
        DataColumn(Text("Type energie", color="white", weight="bold", size=12)),
        DataColumn(Text("Type reservoir", color="white", weight="bold", size=12)),
        DataColumn(Text("V reservoir", color="white", weight="bold", size=12)),
        DataColumn(Text("Etat", color="white", weight="bold", size=12)),
        DataColumn(Text("Cause panne", color="white", weight="bold", size=12)),
        DataColumn(Text("Observation", color="white", weight="bold", size=12)),
        DataColumn(Text("Date", color="white", weight="bold", size=12)),
    ],
    rows=[]
)

Mytable = Column(
    scroll="auto",
    controls=[
        Row([tb], scroll="always")
    ]
)
