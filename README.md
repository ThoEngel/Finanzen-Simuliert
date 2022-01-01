## Rentenplanung
Tool zur Rentenplanung

Das Python Tool dient zur Bestimmung der sicheren Entnahmeraten aus einem Weltportfolio:

* Beliebige Generierung von Vermögensrenditen (historische S&P500, Monte Carlo)
* Beliebige Vermögensallokationsstrategien
* Beliebige Entnahmestrategie (feste Entnahme, variabler Prozentsatz)

Die Ideen und Ansätze für diese frei zugängliche Implementierung basieren auf Website: [Finanzen? Erklärt!](https://www.finanzen-erklaert.de/)

##Datengrundlage
Die Datengrundlage für die montliche Berechnungen basieren auf dem S&P500 Daten. Diese Daten inkl. der Inflation sind auf der Webseite:
[Early Retirement Now](https://earlyretirementnow.com/2018/08/29/google-sheet-updates-swr-series-part-28/) als Excel Tabelle verfügbar.

Mit dem Python-Skript [ReadExel.py](https://github.com/ThoEngel/rentenplanung/blob/main/ReadExcel.py) werden die benötigen Daten extrahiert
in eine Pickle-Datenstruktur exportiert:

```
print(return_df.head())

   month    year    stocks       cpi        cap
0    1.0  1900.0  0.016413  0.000000  18.674275
1    2.0  1900.0  0.008983  0.012048  18.703797
2    3.0  1900.0  0.011084  0.000000  18.775793
3    4.0  1900.0  0.015894  0.000000  18.936402
4    5.0  1900.0 -0.020935 -0.023809  18.403197
....

```



Quelle: 
[Vorsicht vor der 4% Regel]( https://www.finanzen-erklaert.de/vorsicht-vor-der-4-regel/)
[Early Retirement Now](https://earlyretirementnow.com/2018/08/29/google-sheet-updates-swr-series-part-28/


