## Rentenplanung
Tool zur Rentenplanung

Das Python Tool dient zur Bestimmung der sicheren Entnahmerate aus einem Weltportfolio:

* Beliebige Generierung von Vermögensrenditen (historische S&P500, Monte Carlo)
* Beliebige Vermögensallokationsstrategien
* Beliebige Entnahmestrategie (feste Entnahme, variabler Prozentsatz)

Die Ideen und Ansätze für diese frei zugängliche Implementierung basieren auf der Website: [Finanzen? Erklärt!](https://www.finanzen-erklaert.de/)

## 1. Datengrundlage
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
## 2. Vorsicht vor der 4% Regel
Die folgende Implementierung und Auswertung bezieht sich auf den [Finanzen?Erklärt! Blog](https://www.finanzen-erklaert.de/) Artikel:  [Vorsicht vor der 4% Regel]( https://www.finanzen-erklaert.de/vorsicht-vor-der-4-regel/)

## 2.1. Analyse der 4% Regel
Im Oktober 1994 wurde die [Trinity-Studie](http://www.retailinvestor.org/pdf/Bengen1.pdf) durch William Bengen veröffentlich. Diese Studie, besser bekannt unter der 4%-Regel 
wird im folgenden mit Hilfe der o. g. Daten validiert. 
Im Gegensatz zu der Trinity-Studie wird der Aktienanteil auf 100% gesetzt, da Anleihen aktuell sowie in der Zukunft wohl keine oder nur geringe Rendite bringen.

Mit dem Python-Skript [Entnahmesimulation.py](https://github.com/ThoEngel/rentenplanung/blob/main/Entnahmesimulation.py) wird die 4% Regel für unterschiedliche Laufzeiten berechnet.
Das folgende Bild zeigt die Fehlerquote der 4%-Regel über eine Laufzeit von 0-100 Jahren.

![Fehlerquote der 4% Regel nach Laufzeit mit Inflationsanpassung](docu/Fehlerquote4ProzentRegel.png)

### 2.2. Sichere Entnahmerate 
Das folgende Bild zeigt die Auswertung der sicheren Entnahmerate nach Laufzeit sowie in Abhängigkeit von vier verschiedenen Fehlerquoten:

![Sichere Entnahme nach Laufzeit sowie Fehlerquoten](docu/SichereEntnahmerate.png)

Das Python-Skript [Entnahmesimulation.py](https://github.com/ThoEngel/rentenplanung/blob/main/SichereEntnahme.py) berechnet für jede Laufzeit sowie Fehlerquote die maximal mögliche Entnahmerate.
Diese Berechnung der Entnahmerate erfolgt über eine Optimierung der sogenannten sukzessiven Approximation (schrittweise Annäherung).

### 2.3. Forward-Entnahmerate
Bei der Berechnung der Forward-Entnahmerate wird berechnet, wie sich ein verzögerter Start der Entnahmephase auf die Entnahmerate auswirkt. 
Die folgende Implementierung und Auswertung bezieht sich auf den [Finanzen?Erklärt! Blog](https://www.finanzen-erklaert.de/) Artikel: [Mit der Forward-Entnahmerate steigert Jana ihr Budget um 38%](https://www.finanzen-erklaert.de/forward-entnahmerate/)

Da bei der Auswertung die Ruhephase von 0 ... 20 Jahren und die Entnahmephase bei 20, 30, 40, 50 und 60 Jahren berechnet wird,
sind somit insgesamt 21 x 5 = 105 Optimierung durchzuführen. In einem Optimierungslauf werden alle 1440 Epochen (01/1900 - 12/2020) mit der jeweilige Laufzeit (Ruhephase + Entnahmephase) berechnet. 
Dies ist sehr rechenintensiv und wurde daher auf die einzelnen Rechenkerne aufgeteilt. 
 

Mit dem Python-Skript [ForwardEntnahmerate.py](https://github.com/ThoEngel/rentenplanung/blob/main/ForwardEntnahmerate.py) werden die folgenden Entnahmen in Abhängigkeit der Entnahmedauer sowie der Ruhephase berechnet:

```
Ergebnis: Forward Entnahmeraten in Abhängigkeit der Ruhephase (Zeile) sowie der Entnahmephase (Spalte):
+----+----------+----------+----------+----------+---------+
|    |       20 |       30 |       40 |       50 |      60 |
|----+----------+----------+----------+----------+---------|
|  0 |  3.30835 |  2.87036 |  2.76929 |  2.6626  | 2.61768 |
|  1 |  3.36807 |  2.96898 |  2.85836 |  2.76314 | 2.69207 |
|  2 |  3.47691 |  3.12324 |  2.99866 |  2.87848 | 2.824   |
|  3 |  3.81949 |  3.43738 |  3.30118 |  3.15854 | 3.1055  |
|  4 |  4.15037 |  3.73218 |  3.59998 |  3.43121 | 3.36434 |
|  5 |  4.42428 |  4.01835 |  3.84651 |  3.64753 | 3.5821  |
|  6 |  4.76108 |  4.34243 |  4.12933 |  3.93618 | 3.87266 |
|  7 |  5.0171  |  4.58389 |  4.35353 |  4.14165 | 4.0795  |
|  8 |  5.22834 |  4.80592 |  4.55004 |  4.34271 | 4.2543  |
|  9 |  5.59992 |  5.171   |  4.85594 |  4.64229 | 4.57031 |
| 10 |  5.99338 |  5.52076 |  5.17672 |  4.93207 | 4.86245 |
| 11 |  6.42589 |  5.91816 |  5.50591 |  5.25002 | 5.18298 |
| 12 |  6.98547 |  6.43645 |  5.92747 |  5.68508 | 5.62157 |
| 13 |  7.85704 |  6.97449 |  6.40815 |  6.28035 | 6.19861 |
| 14 |  8.61201 |  7.31861 |  6.74751 |  6.60467 | 6.5266  |
| 15 |  8.97479 |  7.62647 |  7.05084 |  6.91443 | 6.83986 |
| 16 |  9.41228 |  7.95342 |  7.39093 |  7.26171 | 7.15855 |
| 17 | 10.0989  |  8.47883 |  7.9219  |  7.78563 | 7.67256 |
| 18 | 10.9359  |  9.08686 |  8.54835 |  8.39948 | 8.2701  |
| 19 | 11.9926  |  9.87123 |  9.3027  |  9.14663 | 8.99534 |
| 20 | 13.4588  | 10.991   | 10.4012  | 10.1925  | 9.99393 |
+----+----------+----------+----------+----------+---------+

Simulationsdauer: 25646 sec. = ca. 7 Std.
```

Das folgende Bild zeigt die o. g. Entnahmerate grafisch an.

![ForwardEntnahmerate](docu/ForwardEntnahmerate.png)



## 3. Berücksichtigung von zukünftigen Assets bei der Rentenplanung
Innerhalb des Erwerbslebens werden Rentenpunkte gesammelt. Diese Rentenpunkte ergeben mit dem aktuellen Rentenwert (2021: 34,19€ in Westdeutschland) eine monatliche Rente.
Diese wird ab dem Rentenalter (in der Regel ab 67 Jahren) ausgezahlt. Eine zusätzliche monatliche Rente hat einen Einfluss auf die Entnahmerate, da ab Rentenbeginn weniger aus dem Depot entnommen werden muss. 

Im Folgenden werden die Python-Skripte um eine zusätzliche Komponente der gesetzlichen Rente erweitert. 

Hierfür wird die bereits eingeführte Konfiguration um die Renten-Konfiguration (_pension_) erweitert:

```
config = {
    'date': {'start': mDate(1, 2022)},
    'assets': {'depot': 500000,
               'fees': 0.20},
    'pension': {'point': np.array([46.0, 31.5]),
                'start_date': [mDate(12, 2038), mDate(12, 2041)],
                'name': {'John Doe', 'Jane Doe'},
                'point_value': 34.19,
                'point_value_inc': 0.5},
    'simulation': {'returns_df': real_return_df,
                   'n_ret_years': 30},
    'invest': {'date': [mDate(1, 2041)],
               'amount': np.array([500000.0])}, 
               'description': {'Erbe'}  
    'withdrawal': {'fixed_pct': 4.0},
    'visualization': {'textoutput': True}    
}
```

Diese Rentenkonfiguration beinhaltet die bereits erworbenen Rentenpunkte (_point_), den Starttermin der gesetzlichen Rente (_start_date_), den Namen der rentenberechtigen Person, die Rentenpunktwert (_point_value_) sowie die jährliche prozentuale Steigerung der Rentenpunktwertes (_point_value_inc_).
Bei den genannten Werten handelt es sich bis auf dem Rentenpunktwert und Steigerung alles um Vektoren, um mehrere Rentenzahlungen zu berücksichtigen (z. B. Mann und Frau zu unterschiedlichen Zeitpunkten mit unterschiedlichen Rentenbeträgen).

Neben der Rente können auch sonstige Zuflüsse (z. B. Auszahlung Lebensversicherung, Immobilienverkäufe, Erben, usw.) berücksichtigt werden. 
Diese werden ebenfalls in der Konfiguration unter (_invest_) entsprechend berücksichtigt und beinhalten das Zahldatum (_date_), den Betrag (_amount_) sowie eine kurze Beschreibung (_description_).
Ähnlich wie bei der Rente können an dieser Stelle mehrere Einträge in Form eines Vektors erfolgen. 


### 3.1. Simulationsszenario: Kann Mad (42) ab sofort in Rente gehen?
Die folgende Implementierung und Auswertung bezieht sich auf den [Finanzen?Erklärt! Blog](https://www.finanzen-erklaert.de/) Artikel:  [Kann Mad (42) ab sofort in Rente gehen?](https://www.finanzen-erklaert.de/kann-mad-ab-sofort-in-rente-gehen/)

Coming soon ....

**Quellen**: 

[Finanzen?Erklärt!](https://www.finanzen-erklaert.de/) 

[Early Retirement Now](https://earlyretirementnow.com/2018/08/29/google-sheet-updates-swr-series-part-28/)

[Trinity Studie: Determining Withdrawal Rates Using Historical Data](http://www.retailinvestor.org/pdf/Bengen1.pdf)



