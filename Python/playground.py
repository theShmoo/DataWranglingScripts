"""Playground for the data wrangler."""
import datawrangler as dw


dw.split_csv("Datenqualitaet_PV.csv",
             "Datenqualitaet_PV_1.csv",
             "Datenqualitaet_PV_2.csv")
