'''
Funktion zur Berechnung der Einkommenssteuer incl. Prognose über die nächsten 60 Jahre

Input:
    zVE: zu versteuerndes Jahreseinkommen
    year: Jahrnummer
            0 akutelles Jahr 2019
            1 Jahr 2020
            .. usw.
            60 max. mögliche Dauer

Output:
    Est: Jährliche Einkommenssteuer
    Tarifzonen:
        Betrag Zone1 - Grundfreibetrag
        Betrag Zone2 - Ende Tarifzone 2
        Betrag Zone3 - Schwelle Spitzensteuersatz

'''

from math import floor
from numpy import polyval, array

def CalEst_Forecast(zvE, year):

    year = min(year, 60)
    year = max(year, 0)

    year = year + 2019

    # Polynom Koeffizenten (3 Ordnung)
    p1 = array([0.0125097582829259, -75.2116286829691, 150889.370192136, -101004178.259542])
    p2 = array([0.00132880431087791, -5.50790732788073, 6205.17661187027, -997977.921678440])
    p3 = array([0.0103662755911936, -62.1393739929084, 124561.449027696, -83446884.4329342])

    # Berechnung der Tarifzonen anhand Polynom
    x1 = polyval(p1, year)
    x2 = polyval(p2, year)
    x3 = polyval(p3, year)
    x4 = 270500

    # Prozentwerte der Tarifzonen
    z1 = 0.14
    z2 = 0.24
    z3 = 0.42
    z4 = 0.45

    zvE = floor(zvE)

    # Berecnhung der Einkommenssteuer
    if zvE <= x1:
        ESt = 0
    elif zvE <= x2:
        ESt = (z2 - z1) / (2 * (x2 - x1)) * (zvE - x1) ** 2 + z1 * (zvE - x1)

    elif zvE <= x3:
        Est2 = (z2 - z1) / (2 * (x2 - x1)) * (x2 - x1) ** 2 + z1 * (x2 - x1)
        ESt = (z3 - z2) / (2 * (x3 - x2)) * (zvE - x2) ** 2 + z2 * (zvE - x2) + Est2
    elif zvE <= x4:
        Est2 = (z2 - z1) / (2 * (x2 - x1)) * (x2 - x1) ** 2 + z1 * (x2 - x1)
        Est3 = (z3 - z2) / (2 * (x3 - x2)) * (x3 - x2) ** 2 + z2 * (x3 - x2) + Est2
        ESt = z3 * (zvE - x3) + Est3
    else:
        Est2 = (z2 - z1) / (2 * (x2 - x1)) * (x2 - x1) ** 2 + z1 * (x2 - x1)
        Est3 = (z3 - z2) / (2 * (x3 - x2)) * (x3 - x2) ** 2 + z2 * (x3 - x2) + Est2
        Est4 = z3 * (x4 - x3) + Est3
        ESt = z4 * (zvE - x4) + Est4

    Tarifzone = {
        'Zone1': x1,
        'Zone2': x2,
        'Zone3': x3,
    }

    return floor(ESt), Tarifzone
