export const MARKT_GEMIDDELD    = 5.8
export const DEFAULT_WACHTDAGEN = 30
export const WACHTDAGEN_OPTIES  = [10, 20, 30, 65, 130, 261]

const OUR_RATES = {
  10:  3.684,
  20:  3.157,
  30:  3.157,
  65:  2.822,
  130: 2.103,
  261: 1.360,
}

export function calculateFysio(loonsom, wachtdagen, currentPct = MARKT_GEMIDDELD) {
  const ourRate      = OUR_RATES[wachtdagen] ?? OUR_RATES[DEFAULT_WACHTDAGEN]
  const onzePremie   = loonsom * (ourRate / 100)
  const huidigePremie = loonsom * (currentPct / 100)
  const besparing    = Math.max(0, huidigePremie - onzePremie)
  const besparingPct = huidigePremie > 0 ? Math.max(0, (besparing / huidigePremie) * 100) : 0
  return { ourRate, onzePremie, huidigePremie, besparing, besparingPct }
}

export function formatCurrency(value) {
  return new Intl.NumberFormat('nl-NL', {
    style: 'currency',
    currency: 'EUR',
    maximumFractionDigits: 0,
  }).format(value)
}
