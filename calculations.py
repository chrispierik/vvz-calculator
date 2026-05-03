VERZUIM_RATES = {
    "0-1%":        {2: 2.399, 4: 2.056, 6: 1.837, 13: 1.369, 26: 0.886, 52: 0.384},
    "1-2%":        {2: 2.827, 4: 2.423, 6: 2.165, 13: 1.614, 26: 1.044, 52: 0.453},
    "2-3%":        {2: 3.255, 4: 2.790, 6: 2.493, 13: 1.858, 26: 1.202, 52: 0.521},
    "3-4%":        {2: 3.684, 4: 3.157, 6: 2.822, 13: 2.103, 26: 1.360, 52: 0.590},
    "4-5%":        {2: 4.112, 4: 3.524, 6: 3.150, 13: 2.347, 26: 1.518, 52: 0.658},
    "5-6%":        {2: 4.540, 4: 3.891, 6: 3.478, 13: 2.592, 26: 1.676, 52: 0.727},
    "6-7%":        {2: 4.969, 4: 4.258, 6: 3.806, 13: 2.836, 26: 1.834, 52: 0.795},
    "7-8%":        {2: 5.397, 4: 4.625, 6: 4.134, 13: 3.081, 26: 1.993, 52: 0.864},
    "8% of hoger": None,
}

WACHTWEKEN_OPTIES = [2, 4, 6, 13, 26, 52]
VERZUIM_KLASSEN   = list(VERZUIM_RATES.keys())


def calculate_fysio(loonsom, verzuimklasse, wachtweken, huidige_premie=0):
    rates = VERZUIM_RATES.get(verzuimklasse)
    if rates is None:
        return None
    rate      = rates[wachtweken]
    onze      = loonsom * (rate / 100)
    besparing = (huidige_premie - onze) if huidige_premie > 0 else None
    bes_pct   = (besparing / huidige_premie * 100) if besparing is not None else None
    return {
        "rate":          rate,
        "onzePremie":    onze,
        "huidigePremie": huidige_premie if huidige_premie > 0 else None,
        "besparing":     besparing,
        "besparingPct":  bes_pct,
    }


def format_currency(value):
    return "€ " + f"{int(round(value)):,}".replace(",", ".")


def format_number(value):
    return f"{int(value):,}".replace(",", ".")
