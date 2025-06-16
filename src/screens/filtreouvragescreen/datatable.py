from flet import *

tb = DataTable(
    columns=[
        # DataColumn(Text("Actions", color="white",
        #            weight="bold", text_align=TextAlign.CENTER, size=12)),
        DataColumn(Text("type", color="white",
                   weight="bold", text_align=TextAlign.CENTER, size=12)),
        DataColumn(Text("prefecture", color="white", weight="bold", size=12)),
        DataColumn(Text("commune", color="white", weight="bold", size=12)),
        DataColumn(Text("canton", color="white", weight="bold", size=12)),
        DataColumn(Text("localite", color="white",weight="bold", text_align=TextAlign.CENTER, size=12)),
        DataColumn(Text("N° Irh", color="white",weight="bold", size=12)),
        DataColumn(Text("nombre", color="white", weight="bold", size=12)),
        DataColumn(Text("Lieu", color="white", weight="bold", size=12)),
        DataColumn(Text("type_energie", color="white", weight="bold", size=12)),
        DataColumn(Text("type_reservoir", color="white", weight="bold", size=12)),
        DataColumn(Text("volume_reservoir", color="white", weight="bold", size=12)),
        DataColumn(Text("etat", color="white", weight="bold", size=12)),
        DataColumn(Text("cause_panne", color="white", weight="bold", size=12)),
        DataColumn(Text("observation", color="white", weight="bold", size=12)),
        DataColumn(Text("created_at", color="white", weight="bold", size=12)),
    ],
    rows=[]
)

Mytable = Column(
    scroll="auto",
    controls=[
        Row([tb], scroll="always")
    ]
)
