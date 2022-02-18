'''
Vorsicht vor der 4% Regel (Teil 3) – welchen Einfluss haben Steuern auf die sichere Entnahmerate?

Sichere Entnahmerate mit Steuer

https://www.finanzen-erklaert.de/vorsicht-vor-der-4-regel-teil-3-welchen-einfluss-haben-steuern-auf-die-sichere-entnahmerate/

'''

import pandas as pd
import time
import plotly.express as px
from SEsimulation.CalEst_Forecast import CalEst_Forecast

startTime = time.time()

# Auswertebereiche
years = range(2019, 2080, 1)            # Jahre

# Datenstruktur
meanTax = pd.DataFrame(columns=['Grundfreibetrag','Ende Tarifzone 2','Schwelle Spitzensteuersatz'], index=years)

column_indexer = 0

# Auswertung der Steuertarifzonen über die Jahre 2019 - 2079
for year in years:

    # Berechnung der Tarifzonen
    Est, Tarifzone = CalEst_Forecast(60000, year - 2019)

    # In Datenstruktur abspeichern
    meanTax.iloc[column_indexer, 0] = Tarifzone['Zone1']
    meanTax.iloc[column_indexer, 1] = Tarifzone['Zone2']
    meanTax.iloc[ column_indexer, 2] = Tarifzone['Zone3']
    column_indexer += 1

# Auswertung Durchschnittssteuersatz über die Jahre sowie über Einkommenshöhen
column_indexer = 0
row_indexer = 0
zvEs = [25000, 50000, 75000, 100000]    # zu versteuerndes Einkommen

# Datenstruktur
tarifTax = pd.DataFrame(columns=zvEs, index=years)

for zvE in zvEs:
    for year in years:
        Est, Tarifzone = CalEst_Forecast(zvE, year-2019)

        # Update Laufzeit
        tarifTax.iloc[row_indexer, column_indexer] = 100 * Est / zvE
        row_indexer += 1

    column_indexer +=1
    row_indexer = 0

# Visulisierung des Durchschnittssteuersatzes
fig = px.line(tarifTax)
fig.update_layout(
    title="Angenommene Entwicklung des Durchschnittssteuersatzes für vers. Einkommenshöhen",
    xaxis_title="Jahre",
    yaxis_title="Durchschnittssteuersatz [%]",
    legend_title="Kapital [€]",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    )
)
fig.show()

# Visulisierung der Tarifzonen
fig = px.line(meanTax)
fig.update_layout(
    title="Angenommene Entwicklung der Tarifzonen im Einkommenssteuertarif",
    xaxis_title="Jahre",
    yaxis_title="Tarifzone [€]",
    legend_title="Tarifzonen",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    )
)
fig.show()

endTime = time.time()
print('\nSimulationsdauer: %5.2f sec.' % (endTime - startTime))