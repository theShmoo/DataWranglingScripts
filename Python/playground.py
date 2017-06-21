"""Playground for the data wrangler."""
import datawrangler as dw


dw.splitCSV("Datenqualitaet_PV.csv",
            ["Datenqualitaet_PV_1.csv",
             "Datenqualitaet_PV_2.csv",
             "Datenqualitaet_PV_3.csv",
             "Datenqualitaet_PV_4.csv"],
            "excel-semicolon")

dw.mergeCSVs(["Datenqualitaet_PV_1.csv",
              "Datenqualitaet_PV_2.csv",
              "Datenqualitaet_PV_3.csv",
              "Datenqualitaet_PV_4.csv"],
             "Datenqualitaet_PV_merged.csv",
             "excel-semicolon")

if dw.areEqualCSV(["Datenqualitaet_PV.csv", "Datenqualitaet_PV_merged.csv"],
                  False):
    print("are equal!")
else:
    print("not equal!")
