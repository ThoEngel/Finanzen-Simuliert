'''
Entnahmestrategien optimieren – bessere Rente dank CAPE Ratio

https://www.finanzen-erklaert.de/entnahmestrategien-optimieren-bessere-rente-dank-cape-ratio/

'''

import pandas as pd
import time
from SEsimulation.mDate import mDate
from SEsimulation import SEsimulation
import plotly.express as px

import plotly.graph_objects as go
from plotly.subplots import make_subplots


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
    while (deltaWidthdrawal > accuracy):
        cnt += 1

        s.withdrawal['fixed_pct'] = percWidthdrawal

        s.init_simulation_onetrial()
        s.simulate_onetrial()

        survival = s.latest_simulation[0]['exhaustion']
        if survival == 60*12:
            curProb = 0
        else:
            curProb = 100

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


if __name__ == "__main__":

    print('Start: Entnahmestrategien optimieren – bessere Rente dank CAPE Ratio')
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
                       'n_ret_years': 60},             # Simulationsdauer in Jahren
        'withdrawal': {'fixed_pct': 4.0},              # Proz. Entnahmerate pro Jahr vom Startdepot
        'visualization': {'textoutput': False}          # Textueller Zwischenausgaben als Debug Info
    }

    err_rate = 0.0        # Fehlerraten [%]

    df = pd.DataFrame(columns = ['Entnahmerate', 'CAPE'], index = range(1, 1453, 1))

    # Optimierungsgrenzen der proz. Entnahme:
    loBound = 2              # Untere Grenze der Optimierung
    hiBound = 16              # Obere Grenze der Optimierung

    # Update Laufzeit

    years = range(1900, 2021, 1)
    months = range(1, 13, 1)

    row_indexer = 0

    for year in years:
        for month in months:
            config['date']['start'] = mDate(month, year)
            config['date']['start_retirement'] = mDate(month, year)

            localstarttime = time.time()

            s = SEsimulation.SEsimulation(config)
            widthdraw = optimize(s, err_rate, loBound, hiBound)

            print('\n', row_indexer, ': ', month, '/', year, ' Entnahme: ', widthdraw, '%  @Risk: ', err_rate, '%')
            print('\n Druchlauf Dauer: %5.2f sec.\n' % (time.time() - localstarttime))

            df.iloc[row_indexer, 0] = widthdraw
            tmp = s.latest_simulation[0]['trial']['cape']
            df.iloc[row_indexer, 1] = tmp.iloc[0]
            row_indexer += 1


    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=df.index, y=df['Entnahmerate'], name="Entnahmerate [%]"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=df.index, y=df['CAPE'], name="CAPE [-]"),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(title_text="Sichere Entnahmerate kalibriert auf den S&P 500 TR real nach CAPE Ratio")

    # Set x-axis title
    fig.update_xaxes(title_text="Zeit [Monate]")

    # Set y-axes titles
    fig.update_yaxes(title_text="Sichere Entnahme [%]", secondary_y=False)
    fig.update_yaxes(title_text="CAPE [-]", secondary_y=True)
    fig.show()

    fig = px.scatter(df, y='Entnahmerate', x='CAPE')

    fig.update_layout(
        title="Sichere Entnahmerate kalibriert auf den S&P 500 TR real nach CAPE Ratio",
        xaxis_title="CAPE Ration [-]",
        yaxis_title="Sichere Entnahme [%]",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        )
    )
    fig.show()

    endTime = time.time()
    print('\nSimulationsdauer: %5.2f sec.' % (endTime - starttime))
