'''
Erkennen, wenn die Pleite droht – besteht während der Entnahmephase Handlungsbedarf?

https://www.finanzen-erklaert.de/wann-besteht-in-der-entnahmephase-handlungsbedarf/

'''

import pandas as pd
import time
from SEsimulation.mDate import mDate
from SEsimulation import SEsimulation
import plotly.graph_objects as go
from plotly.subplots import make_subplots

if __name__ == "__main__":

    print('Start: Erkennen, wenn die Pleite droht – besteht während der Entnahmephase Handlungsbedarf?')
    starttime = time.time()

    # Lesen monatliche S&P500 Daten
    RETURN_FILE = 'real_return_df.pickle'
    real_return_df = pd.read_pickle(RETURN_FILE)

    # Konfiguration der Entnahme Simulation
    config = {
        'date': {'start': mDate(1, 2022),             # Start Datum
                 'start_retirement': mDate(1, 2022)},           # Start der Entnahme
        'assets': {'depot': 100,                       # Depotvolumen zum Startzeitpunkt
                   'fees': 0.00},                      # Jährliche Depotgebühren in %
        'simulation': {'returns_df': real_return_df,   # S&P500 Daten
                       'n_ret_years': 30},             # Simulationsdauer in Jahren
        'withdrawal': {'fixed_pct': 4.0},              # Proz. Entnahmerate pro Jahr vom Startdepot
        'visualization': {'textoutput': False}          # Textueller Zwischenausgaben als Debug Info
    }

    years = range(1900, 2020, 1)
    months = range(1, 13, 1)

    allresults = pd.DataFrame()
    negresults = pd.DataFrame()
    posresults = pd.DataFrame()

    nretyears = config['simulation']['n_ret_years'] * 12

    for year in years:
        for month in months:

            config['date']['start'] = mDate(month, year)
            config['date']['start_retirement'] = mDate(month, year)

            s = SEsimulation.SEsimulation(config)
            s.init_simulation_onetrial()
            s.simulate_onetrial()

            if s.latest_simulation[0]['exhaustion'] == nretyears:
                posresults = posresults.append(s.latest_simulation[0]['trial'].end_port)
            else:
                negresults = negresults.append(s.latest_simulation[0]['trial'].end_port)

            allresults.append(s.latest_simulation)

    fig = make_subplots()

    # Add traces
    fig.add_trace(go.Scatter(x=posresults.min().index, y=posresults.min(), name="vorzeitige Pleite"))

    fig.add_trace(go.Scatter(x=negresults.max().index, y=negresults.max(), name="sicherer Hafen"))

    # Add figure title

    perc = s.withdrawal['fixed_pct']
    year = s.simulation['n_ret_years']
    text = "{}%-Regel über {} Jahre - Wann bin ich auf der sicheren Seite?".format(perc, year)
    fig.update_layout(title_text = text)

    # Set x-axis title
    fig.update_xaxes(title_text="Monate in Entnahmephase")

    # Set y-axes titles
    fig.update_yaxes(title_text="Kapital in % vom Startkapital (real)")

    fig.show()

    endTime = time.time()
    print('\nSimulationsdauer: %5.2f sec.' % (endTime - starttime))
