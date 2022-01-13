from SEsimulation.mDate import mDate
import numpy as np
import pandas as pd
import copy

from dataclasses import dataclass, field
from typing import List

@dataclass
class Trialdata:
    """
    Class
    """

    spend: float = 0
    portval: float = 100

    inflation: List[float] = field(default_factory=list)
    months: List[int] = field(default_factory=list)
    cape: List[int] = field(default_factory=list)
    end_ports: List[float] = field(default_factory=list)
    spends: List[float] = field(default_factory=list)
    trial_df: pd.DataFrame = None


class SEsimulation():
    """Entnahmesimulation
    Sichere Entnahme für den Ruhestand (SE)
    """

    def __init__(self, config):
        """initialize simulation from a config dict

        Args:
            config (dict): date, assets, simulation, withdrawal
        """

        self.date = config.get('date')
        self.init_date()

        self.assets = config.get('assets')
        self.init_assets()

        self.simulation = config.get('simulation')
        self.init_simulation()

        self.withdrawal = config.get('withdrawal')
        self.init_withdrawal()

        self.visualization = config.get('visualization')
        self.init_visualization()

        self.latest_trial = Trialdata()
        self.latest_simulation = []

    def init_date(self):
        """initialize for date
        """
        pass


    def init_assets(self):
        """initialize for assets
        """
        pass

    def init_simulation(self):
        """initialize / reinitialize simulation based on configs

        Raises:
            Exception: bad values

        """
        #self.simulation['n_asset_years'], self.simulation['n_assets'] = self.simulation['returns_df'].shape
        self.simulation['trials'] = self.historical_trials()

    def init_simulation_onetrial(self):
        """initialize / reinitialize simulation based on configs

        Raises:
            Exception: bad values

        """

        self.simulation['trials'] = self.historical_onetrial()


    def init_withdrawal(self):
        """initialize for withdrawal based on configs
        """
        pass

    def init_visualization(self):
        """initialize for visualization based on configs
        """
        pass


    def get_withdrawal(self):
        """return withdrawal for current iteration

        Returns:
            float: withdrawal for current iteration
        """

        desired_withdrawal = self.assets['depot'] * self.withdrawal['fixed_pct'] / 100

        return desired_withdrawal

    def eval_trial(self):
        """compute all metrics and return in dict

        Returns:
            dict: key = name of metric, value = metric
        """

        min_end_port_index = int(np.argmin(self.latest_trial.end_ports))
        min_end_port = self.latest_trial.end_ports[min_end_port_index]
        exhaustion = min_end_port_index if min_end_port == 0.0 else self.simulation['n_ret_years'] * 12

        return {'exhaustion': exhaustion,
                'min_end_port': min_end_port,
                'min_end_port_index': min_end_port_index
                }
    
    def historical_trial_generator(self, idxDate):
        """
        für jeden Startzeitpunkt eine Epoche: StartPunkt bis (StartPunkt + n_ret_years) generieren
        """

        df = self.simulation['returns_df']
        n_ret_months = self.simulation['n_ret_years'] * 12
        num_of_months = len(df.index)

        cnt = 0
        while cnt < n_ret_months:
            if (idxDate + cnt) < num_of_months:
                yield tuple(df.iloc[idxDate + cnt])
            else:
                idxDate = -cnt  # Von vorne wieder beginnen
                yield tuple(df.iloc[idxDate + cnt])
            cnt += 1

    def historical_trials(self):
        """
        jeden historischen Startzeitpunkt generieren (1900 - 2020) * 12 = 1440 Monate als Startzeitpunkte
        """

        df = self.simulation['returns_df']

        num_of_dates = len(df.index)

        for idxDate in range(0, num_of_dates):
            yield self.historical_trial_generator(idxDate)

    def historical_onetrial(self):
        """
        eine Epoche für einen Zeitpunkt generieren
        """

        df = self.simulation['returns_df']

        # Startzeitpunkte holen
        Date = self.date['start']
        month = Date.Month
        year = Date.Year

        # Index des Startzeitpunktes berechnen
        idx = df.index[(df['month'] == month) & (df['year'] == year)]
        yield self.historical_trial_generator(idx.values[0])


    def simulate_onetrial(self):
        """
        Epoche simulieren und bewerten
        """

        self.latest_simulation = []

        for trial in self.simulation['trials']:
            trial_df = self.simulate_trial(trial)

            # Bewerte die Epoche
            eval_metrics_dict = self.eval_trial()
            df_dict = {'trial': trial_df}
            self.latest_simulation.append({**df_dict, **eval_metrics_dict})
            break
        return self.latest_simulation

    def simulate(self):
        """
        Alle möglichen Epochen simulieren und bewerten
        """

        self.latest_simulation = []

        for trial in self.simulation['trials']:
            trial_df = self.simulate_trial(trial)

            # Bewerte die Epoche
            eval_metrics_dict = self.eval_trial()
            df_dict = {'trial': trial_df}
            self.latest_simulation.append({**df_dict, **eval_metrics_dict})

        return self.latest_simulation

    def simulate_trial(self, trial_rows):
        """
        Simuliere eine Epoche
        """

        self.latest_trial = Trialdata()
        current_trial = self.latest_trial

        # Init Startdepotwert
        current_trial.portval = self.assets['depot']

        # Parameter:
        fees = copy.deepcopy(self.assets['fees'])
        curDate = copy.deepcopy(self.date['start'])
        curStartRetr = copy.deepcopy(self.date['start_retirement'])

        # Inflation
        curInflation = 100

        for i, t in enumerate(trial_rows):

            # Aktuelle S&P500 Werte holen
            month, year, port_return, cpi, cape = int(t[0]), int(t[1]), t[2], t[3], t[4]

            current_trial.months.append(year * 12 + month)
            current_trial.cape.append(cape)

            # Inflation:
            curInflation *= (1 + cpi)
            current_trial.inflation.append(curInflation)

            # Entnahme aus dem Depot
            if curStartRetr <= curDate:  # Entnahme aus dem Depot
                current_trial.spend = min(float(self.get_withdrawal()/12), current_trial.portval)
                current_trial.spends.append(current_trial.spend)
            else:
                current_trial.spend = 0
                current_trial.spends.append(current_trial.spend)

            current_trial.portval = current_trial.portval - current_trial.spend

            # Wertentwicklung des Depots inkl. Gebühren
            current_trial.portval *= (1 + port_return - fees/1200)
            current_trial.end_ports.append(current_trial.portval)

            curDate.DateInc()

        current_trial.trial_df = pd.DataFrame(index=current_trial.months,
                              data={'spend': current_trial.spends,
                                    'end_port': current_trial.end_ports,
                                    'inflation': current_trial.inflation,
                                    'cape': current_trial.cape
                                    })

        return current_trial.trial_df

if __name__ == '__main__':
    print('Executing as standalone script')