from math import floor

def CalEst(zvE):
    # 2020

    x = floor(zvE)
    y = max((x - 9408) / 10000, 0)
    z = max((x - 14532) / 10000, 0)

    if zvE <= 9408:
        ESt = 0
    elif zvE <= 14532:
        ESt = (972.87 * y + 1400) * y

    elif zvE <= 57051:
        ESt = ((212.02 * z + 2397) * z + 972.79)

    elif zvE <= 270500:
        ESt = (0.42 * x - 8963.74)

    else:
        ESt = (0.45 * x - 17078.74)

    Est = floor(ESt)

    return Est
