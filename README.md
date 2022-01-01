## Rentenplanung
Tool zur Rentenplanung

Das Python Tool dient zur Bestimmung der sicheren Entnahmerate aus einem Weltportfolio:

* Beliebige Generierung von Vermögensrenditen (historische S&P500, Monte Carlo)
* Beliebige Vermögensallokationsstrategien
* Beliebige Entnahmestrategie (feste Entnahme, variabler Prozentsatz)

Die Ideen und Ansätze für diese frei zugängliche Implementierung basieren auf der Website: [Finanzen? Erklärt!](https://www.finanzen-erklaert.de/)

## Datengrundlage
Die Datengrundlage für die monatliche Berechnungen basieren auf dem S&P500 Daten. Diese Daten inkl. der Inflation sind auf der Webseite:
[Early Retirement Now](https://earlyretirementnow.com/2018/08/29/google-sheet-updates-swr-series-part-28/) als Excel Tabelle verfügbar.

Diese Daten liegen für einen Zeitraum von 01/1871 bis zum aktuellen Zeitpunkt vor. 

Mit dem Python-Skript [ReadExel.py](https://github.com/ThoEngel/rentenplanung/blob/main/ReadExcel.py) werden die benötigen Daten extrahiert
und in eine Pickle-Datenstruktur exportiert:

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

## Analyse der 4%-Regel
Im Oktober 1994 wurde die [Trinity-Studie](http://www.retailinvestor.org/pdf/Bengen1.pdf) durch William Bengen veröffentlich. Diese Studie, besser bekannt unter der 4%-Regel 
wird im folgenden mit Hilfe der o. g. Daten validiert ...

Coming soon.





**Quelle**: 

[Vorsicht vor der 4% Regel]( https://www.finanzen-erklaert.de/vorsicht-vor-der-4-regel/)

[Early Retirement Now](https://earlyretirementnow.com/2018/08/29/google-sheet-updates-swr-series-part-28/)

[Trinity Studie: Determining Withdrawal Rates Using Historical Data](http://www.retailinvestor.org/pdf/Bengen1.pdf)



