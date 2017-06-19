"""Playground for the data wrangler."""
import datawrangler as dw


dw.splitCSV("Datenqualitaet_PV.csv",
            ["Datenqualitaet_PV_1.csv",
             "Datenqualitaet_PV_2.csv",
             "Datenqualitaet_PV_3.csv"],
            "excel-semicolon")

dw.mergeCSVs(["Datenqualitaet_PV_1.csv",
              "Datenqualitaet_PV_2.csv",
              "Datenqualitaet_PV_3.csv"],
             "Datenqualitaet_PV_merged.csv",
             "excel-semicolon")

dw.areEqualCSV(["Datenqualitaet_PV.csv", "Datenqualitaet_PV_merged.csv"])
