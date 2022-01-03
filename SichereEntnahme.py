'''
Vorsicht vor der 4%-Regel

Sicher Entnahmerate

https://www.finanzen-erklaert.de/vorsicht-vor-der-4-regel/

'''

import pandas as pd
import time
from SEsimulation.mDate import mDate
from SEsimulation import SEsimulation
import plotly.express as px

def optimize(s, probability, loBound, hiBound):
    """ Optimiere auf die max. mögliche Entnahme bei einer vorgegebenen Fehlerquote

    Returns:
        widthdrawal: max. mögliche prozentuale Entnahme
    """

    n_ret_months = s.simulation['n_ret_years'] * 12

    accuracy = 0.01     # Genauigkeit der Optimierung

    # Vorbereitung der Optimierung
    deltaWidthdrawal = (hiBound - loBound) / 2
    percWidthdrawal = loBound + deltaWidthdrawal

    cnt = 0
    curProb = 0

    # Optimization by successiv approximation
    while (deltaWidthdrawal > accuracy) or (curProb > probability):
        cnt += 1

        s.withdrawal['fixed_pct'] = percWidthdrawal

        s.init_simulation()
        s.simulate()

        survival = [trial_dict['exhaustion'] for trial_dict in s.latest_simulation]
        curProb = 100 * (len(survival) - survival.count(n_ret_months)) / len(survival)

        if s.visualization['textoutput'] == True:
            print(cnt, '. Entnahme: ', percWidthdrawal, '  Ausfallwahrscheinlichkeit: ', curProb, '%')

        deltaWidthdrawal /= 2

        if deltaWidthdrawal <= accuracy / 10:
            break

        if curProb > probability:
            percWidthdrawal -= deltaWidthdrawal
        else:
            percWidthdrawal += deltaWidthdrawal

    return percWidthdrawal

print('Start')
starttime = time.time()

# Lesen monatliche S&P500 Daten
RETURN_FILE = 'real_return_df.pickle'
real_return_df = pd.read_pickle(RETURN_FILE)

# Konfiguration der Entnahme Simulation
config = {
    'date': {'start': mDate(1, 2022)},             # Start Datum
    'assets': {'depot': 500000,                    # Depotvolumen zum Startzeitpunkt
               'fees': 0.00},                      # Jährliche Depotgebühren in %
    'simulation': {'returns_df': real_return_df,   # S&P500 Daten
                   'n_ret_years': 30},             # Simulationsdauer in Jahren
    'withdrawal': {'fixed_pct': 4.0},              # Proz. Entnahmerate pro Jahr vom Startdepot
    'visualization': {'textoutput': True}          # Textueller Zwischenausgaben als Debug Info
}

err_rates = [0.0, 0.1, 0.5, 1.0]        # Fehlerraten [%]
years = [10, 12, 14, 16, 18, 20, 22, 25, 28, 31, 35, 39, 44, 49, 55, 60]  # Dauer der Entnahme in Jahre

df = pd.DataFrame(columns=err_rates, index=years)

# Optimierungsgrenzen der proz. Entnahme:
loBound = 2              # Untere Grenze der Optimierung
hiBound = 8              # Obere Grenze der Optimierung

column_indexer = 0

for err_rate in err_rates:
    row_indexer = 0
    hiBound = 8

    for year in years:

        # Update Laufzeit
        config['simulation']['n_ret_years'] = year

        s = SEsimulation.SEsimulation(config)
        widthdraw = optimize(s, err_rate, loBound, hiBound)

        print('\n', year, ' Jahre, Entnahme: ', widthdraw, '%  @Risk: ', err_rate, '%\n')

        df.iloc[row_indexer, column_indexer] = widthdraw
        row_indexer += 1
        hiBound = widthdraw

    column_indexer += 1

fig = px.line(df)

fig.update_layout(
    title="Sichere jährliche Entnahmerate nach Laufzeit mit Inflationsanpassung",
    xaxis_title="Laufzeit [Jahre]",
    yaxis_title="Sichere Entnahme [%]",
    legend_title="Fehlerquote [%]",
    font=dict(
        family="Courier New, monospace",
        size=16,
        color="RebeccaPurple"
    )
)
fig.show()
endTime = time.time()
print('\nSimulationsdauer: %5.2f sec.' % (endTime - starttime))
