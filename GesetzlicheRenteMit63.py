'''
Gesetzliche Rente mit 63 ist immer die richtige Entscheidung

https://www.finanzen-erklaert.de/gesetzliche-rente-mit-63-ist-immer-die-richtige-entscheidung/

'''

import pandas as pd
import time
from SEsimulation.mDate import mDate
from SEsimulation import SEsimulation
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import numpy as np

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

        if deltaWidthdrawal <= accuracy / 4:
            break

        if curProb > probability:
            percWidthdrawal -= deltaWidthdrawal
        else:
            percWidthdrawal += deltaWidthdrawal

    return percWidthdrawal

if __name__ == "__main__":

    print('Gesetzliche Rente mit 63 ist immer die richtige Entscheidung')
    starttime = time.time()

    # Lesen monatliche S&P500 Daten
    RETURN_FILE = 'real_return_df.pickle'
    real_return_df = pd.read_pickle(RETURN_FILE)

    # Konfiguration der Entnahme Simulation
    config = {
        'date': {'start': mDate(1, 2022),              # Start Datum
                 'start_retirement': mDate(1, 2022)},  #Start der Entnahme
        'assets': {'depot': 500000,                    # Depotvolumen zum Startzeitpunkt
                   'fees': 0.00},                      # Jährliche Depotgebühren in %
        'simulation': {'returns_df': real_return_df,   # S&P500 Daten
                       'n_ret_years': 30},             # Simulationsdauer in Jahren
        'withdrawal': {'fixed_pct': 4.0},              # Proz. Entnahmerate pro Jahr vom Startdepot
        'pension': {'point': np.array([30]),           # Anzahl erworbener Rentenpunkte
                    'point_add': np.array([0.0]),      # Rentenpunktzuwachs pro Jahr
                    'start_date': [mDate(1, 2027)],    # Beginn der gesetzlichen Rente
                    'name': {'Mad'},                   # Name des Rentenbeziehers
                    'point_value': 39.14,              # aktueller Rentenpunktwert
                    'point_value_inc': 0.5},           # Proz. Steigerung des Rentenpunktwertes
        'visualization': {'textoutput': False}          # Textueller Zwischenausgaben als Debug Info
    }

    AlterVec = range(40, 61, 1)

    err_rate = 2.5

    loBound = 3.25
    hiBound = 8.0

    df = pd.DataFrame(columns = ['ohneRente', 'mitRente67',  'mitRente63'], index = AlterVec)

    row_indexer = 0

    for alter in AlterVec:

        # 1.
        print('\n1. Szenario: Entnahme mit ', alter, ' Jahren mit gesetzl. Rente ab 67')
        config['simulation']['n_ret_years'] = 100 - alter  # Entnahmedauer
        config['pension']['point'] = np.array([(alter - 25) * 1.5])
        config['pension']['point_add'] = np.array([0])
        config['pension']['start_date'] = [mDate(1, 2022 + (67 - alter))]
        config['pension']['point_value'] = 34.19 * 0

        s = SEsimulation.SEsimulation(config)
        widthdraw1 = optimize(s, err_rate, loBound, hiBound)
        df.iloc[row_indexer, 0] = widthdraw1
        print('\n', alter, ' Jahre alt, Entnahme: ', widthdraw1, '%  @Risk: ', err_rate, '%\n')

        # 2.
        print('\n2. Szenario: Entnahme mit ', alter, ' Jahren mit gesetzl. Rente ab 67')
        config['simulation']['n_ret_years'] = 100 - alter  # Entnahmedauer
        config['pension']['point'] = np.array([(alter - 25) * 1.5])
        config['pension']['point_add'] = np.array([0])
        config['pension']['start_date'] = [mDate(1, 2022 + (67 - alter))]
        config['pension']['point_value'] = 34.19

        s = SEsimulation.SEsimulation(config)
        widthdraw2 = optimize(s, err_rate, loBound, hiBound)
        df.iloc[row_indexer, 1] = widthdraw2 - widthdraw1
        print('\n', alter, ' Jahre alt, Entnahme: ', widthdraw2, '%  @Risk: ', err_rate, '%\n')

        # 3.
        print('\n3. Szenario: Entnahme mit ', alter, ' Jahren mit gesetzl. Rente ab 67')
        config['simulation']['n_ret_years'] = 100 - alter  # Entnahmedauer
        config['pension']['point'] = np.array([(alter - 25) * 1.5])
        config['pension']['point_add'] = np.array([0])
        config['pension']['start_date'] = [mDate(1, 2022 + (63 - alter))]
        config['pension']['point_value'] = 34.19 * 0.856

        s = SEsimulation.SEsimulation(config)
        widthdraw3 = optimize(s, err_rate, loBound, hiBound)
        df.iloc[row_indexer, 2] = widthdraw3 - widthdraw2
        print('\n', alter, ' Jahre alt, Entnahme: ', widthdraw3, '%  @Risk: ', err_rate, '%\n')

        row_indexer += 1

    fig = make_subplots()

    # Add traces
    fig.add_trace(go.Bar(x=df.index, y=df['ohneRente'], name="sichere Entnahmerate@2,5% Risk"))
    fig.add_trace(go.Bar(x=df.index, y=df['mitRente67'], name="sichere Entnahmerate Rente 67 @2,5% Risk"))
    fig.add_trace(go.Bar(x=df.index, y=df['mitRente63'], name="sichere Entnahmerate Rente 63 @2,5% Risk"))

    # Add figure title
    fig.update_layout(title_text="Erhöhung der Entnhamerate durch die gesetzliche Rente regulär ab 67 und ab 63 mit 14,4% Abschlag",
                      barmode='stack')

    # Set x-axis title
    fig.update_xaxes(title_text="Alter & Beginn Entnahmephase")

    # Set y-axes titles
    fig.update_yaxes(title_text="sichere Entnahme [%]")
    fig.show()

    endTime = time.time()
    print('\nSimulationsdauer: %5.2f sec.' % (endTime - starttime))