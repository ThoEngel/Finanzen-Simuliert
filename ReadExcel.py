'''
Monatliche S&P500 Total Return Daten inkl. Inflation einlesen

Daten-Quelle:
https://earlyretirementnow.com/2018/08/29/google-sheet-updates-swr-series-part-28/
https://docs.google.com/spreadsheets/d/1QGrMm6XSGWBVLI8I_DOAeJV5whoCnSdmaR8toQB2Jz8/copy?

Alternative Daten: (jedoch nicht verwendet)
http://www.econ.yale.edu/~shiller/data.htm

'''

import pandas as pd

# Read Excel file with monthly data: month, year, s&p500 total return, cpi, cap , ...
df = pd.read_excel('data\EarlyRetirementNow SWR Toolbox v2.0.xlsx', sheet_name='StockBond Returns', header=4)

# Cut relevant rows and colums
return_df = df.iloc[0:1900, [0, 1, 4, 12, 13]]

# Neue Zeilennummerierung
return_df.index = range(len(return_df))

# Neue Spaltennamen
return_df.columns=['month', 'year', 'cpi', 'cap', 'stocks']

# Berechne prozentuale Inflation pro Monat
cpi = return_df['cpi']
cpi_t1 = cpi.shift()
perc_cpi = (cpi / cpi_t1) - 1

# Neues Datenframe zusammenstellen:
new_df = pd.DataFrame()
new_df['month'] = return_df['month']
new_df['year'] = return_df['year']
new_df['stocks'] = return_df['stocks']
new_df['cpi'] = perc_cpi
new_df['cap'] = return_df['cap']

# Relevanten Daten von 1/1900 bis 01/2021 ausschneiden:

# Start Index ermitteln
idxArr = new_df.index[(new_df['year'] == 1900) & (new_df['month'] == 1)].tolist()
idxStart = idxArr[0]

# End Index ermitteln
idxArr = new_df.index[(new_df['year'] == 2021) & (new_df['month'] == 1)].tolist()
idxEnd = idxArr[0]

return_df = new_df[idxStart:idxEnd]

# Neue Zeilennummerierung
return_df.index = range(len(return_df))

# Schreibe pickle ....
return_df.to_pickle('real_return_df_new.pickle')