'''
Vorsicht vor der 4%-Regel

https://www.finanzen-erklaert.de/vorsicht-vor-der-4-regel/

'''

import pandas as pd
import time
from SEsimulation.mDate import mDate
from SEsimulation import SEsimulation
import plotly.express as px

print('Start')
starttime = time.time()

# Lesen monatliche S&P500 Daten
RETURN_FILE = 'real_return_df.pickle'
real_return_df = pd.read_pickle(RETURN_FILE)

# Konfiguration der Entnahme Simulation
config = {
    'date': {'start': mDate(1, 2022),             # Start Datum
    'start_retirement': mDate(1, 2022)},           # Start der Entnahme
    'assets': {'depot': 500000,                    # Depotvolumen zum Startzeitpunkt
               'fees': 0.00},                      # Jährliche Depotgebühren in %
    'simulation': {'returns_df': real_return_df,   # S&P500 Daten
                   'n_ret_years': 30},             # Simulationsdauer in Jahren
    'withdrawal': {'fixed_pct': 4.0},              # Proz. Entnahmerate pro Jahr vom Startdepot
    'visualization': {'textoutput': True}  # Textueller Zwischenausgaben als Debug Info
}

years = range(1, 101, 1)           # Dauer der Entnahme in Jahre

df = pd.DataFrame(columns=[1], index=years)
row_indexer = 0

for year in years:
    config['simulation']['n_ret_years'] = year

    s = SEsimulation.SEsimulation(config)

    s.simulate()

    survival = [trial_dict['exhaustion'] for trial_dict in s.latest_simulation]
    curProb = 100 * (len(survival) - survival.count(year * 12)) / len(survival)

    print(year, ' Jahre, ', config['withdrawal']['fixed_pct'], '% Entnahme, Ausfallwahrscheinlichkeit: ', curProb, '%')

    df.iloc[row_indexer, 0] = curProb
    row_indexer += 1

fig = px.line(df)

fig.update_layout(
    title="Fehlerquote der 4% Regel nach Laufzeit / mit Inflationsanpassung",
    xaxis_title="Entnahmedauer [Jahre]",
    yaxis_title="Fehlerrate [%]",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    )
)
fig.show()

endTime = time.time()
print('\nSimulationsdauer: %5.2f sec.' % (endTime - starttime))
