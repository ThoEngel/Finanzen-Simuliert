'''
Mit der Forward-Entnahmerate steigert Jana ihr Budget um 38%

https://www.finanzen-erklaert.de/forward-entnahmerate/

'''

import pandas as pd
import time
from SEsimulation.mDate import mDate
from SEsimulation import SEsimulation
import numpy as np
import plotly.express as px
from tabulate import tabulate
import multiprocessing
from multiprocessing import Process

# Funktion zur Optmierung der Entnahmerate
def optimize(s, probability, loBound, hiBound):
    """ Optimiere auf die max. mögliche Entnahme bei einer vorgegebenen Fehlerquote

    Returns:
        widthdrawal: max. mögliche prozentuale Entnahme
    """

    n_ret_months = s.simulation['n_ret_years'] * 12

    accuracy = 0.005     # Genauigkeit der Optimierung

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

        if deltaWidthdrawal <= accuracy / 5:
            break

        if curProb > probability:
            percWidthdrawal -= deltaWidthdrawal
        else:
            percWidthdrawal += deltaWidthdrawal

    return percWidthdrawal

# Funktion zur Berechnung der Forward Entnahmerate
def forward(DauerEntnahme, send_end):

    # Lesen monatliche S&P500 Daten
    RETURN_FILE = 'real_return_df.pickle'
    real_return_df = pd.read_pickle(RETURN_FILE)

    # Simulationskonfiguration
    config = {
        'date': {'start': mDate(1, 2022),  # Startdatum der Simulation
                 'start_retirement': mDate(1, 2022)},  # Start der Entnahme
        'assets': {'depot': 1000000,  # Depotvolumen zum Startzeitpunkt
                   'fees': 0.00},  # Jährliche Depotgebühren in %
        'simulation': {'returns_df': real_return_df,  # S&P500 Daten
                       'n_ret_years': 53},  # Simulationsdauer in Jahren
        'withdrawal': {'fixed_pct': 3.0},  # Proz. Entnahmerate pro Jahr vom Startdepot
        'pension': {'point': np.array([0]),  # Anzahl erworbener Rentenpunkte
                    'point_add': np.array([0.0]),  # Rentenpunktzuwachs pro Jahr
                    'start_date': [mDate(1, 3000)],  # Beginn der gesetzlichen Rente
                    'name': {'John Doe'},  # Name des Rentenbeziehers
                    'point_value': 0.0,  # aktueller Rentenpunktwert
                    'point_value_inc': 0.0},  # Proz. Steigerung des Rentenpunktwertes
        'visualization': {'textoutput': False}  # Textueller Zwischenausgaben als Debug Info
    }

    result = np.array([])       # leeren Ergebnisvektor

    err_rate = 0.0
    hiBound = 13.5
    loBound = 2.5

    Ruhephasen = range(0, 21, 1)  # Dauer der Ruhephase in Jahren

    for Ruhephase in Ruhephasen:
        config['date']['start_retirement'] = mDate(2, 2022 + Ruhephase)
        config['simulation']['n_ret_years'] = Ruhephase + DauerEntnahme

        s = SEsimulation.SEsimulation(config)

        widthdraw = optimize(s, err_rate, loBound, hiBound)

        loBound = widthdraw     # Anpassung der unteren Optimierungsgrenze um den Suchbereich zu verkleinern

        print('\nRuhephase: ', Ruhephase, ' Jahre, Entnahmephase: ', DauerEntnahme, ' Jahre, @Risk: ', err_rate, '%, Entnahmerate: ', widthdraw, '%')

        result = np.append(result, widthdraw)

    send_end.send(result)


if __name__ == "__main__":

    print('Starte - Forward Entnahmerate')
    starttime = time.time()

    Ruhephasen = range(0, 21, 5)
    Entnahmephase = [20, 30, 40, 50, 60]

    # Pipline für Mulicore Precessing
    recv_end, send_end = multiprocessing.Pipe(False)

    pipe_list = []
    jobs = []

    # Starte die einzelnen Job's
    for phase in Entnahmephase:
        p = Process(target=forward, args=(phase, send_end))
        pipe_list.append(recv_end)
        jobs.append(p)
        p.start()

    for proc in jobs:
        proc.join()

    print("Fertig!")
    print('\nSimulationsdauer: %5.2f sec.' % (time.time() - starttime))

    # Ergebnisse Zusammenstellen:
    df = pd.DataFrame(columns=Entnahmephase, index=Ruhephasen)

    for i, x in enumerate(pipe_list):
        vector = x.recv()
        df.iloc[:, i] = vector

    print('\nErgebnis: Forward-Entnahmeraten in Abhängigkeit der Ruhephase (Zeile) sowie der Entnahmephase (Spalte):')
    print(tabulate(df, headers = 'keys', tablefmt = 'psql'))
    print('\n')

    # Ergebnis: Wachstum der Entnahmerate
    df1 = pd.DataFrame(columns=Entnahmephase, index=Ruhephasen)
    for i, row in enumerate(df.columns):
        df1.iloc[:, i] = 100 * df.iloc[:, i].diff() / df.iloc[:, i]

    # Visualisierung der Entnahmerate in Abhängigkeit der Ruhephase sowie der Entnahmephase
    fig = px.line(df)
    fig.update_layout(
        title="Forward-Entnahmeraten in Abhängigkeit der Ruhephase sowie der Entnahmephase",
        xaxis_title="Ruhephase [Jahre]",
        yaxis_title="Entnahmerate [%]",
        legend_title="Entnahmezeit [Jahre]",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        )
    )
    fig.show()

    # Visualisierung Wachstum Entnahmerate
    fig = px.line(df1)
    fig.update_layout(
        title="Forward-Entnahmeraten: Wachstum Entnahmerate",
        xaxis_title="Ruhephase [Jahre]",
        yaxis_title="Wachstum Entnahmerate [%]",
        legend_title="Entnahmezeit [Jahre]",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        )
    )
    fig.show()