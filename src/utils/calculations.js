export function calculate(loonsom, branch) {
  const huidigePremie    = loonsom * (branch.gemiddeld / 100)
  const marktbestePremie = loonsom * (branch.marktbest / 100)
  const geschatBesparing = huidigePremie - marktbestePremie
  const besparingPct     = (geschatBesparing / huidigePremie) * 100
  return { huidigePremie, marktbestePremie, geschatBesparing, besparingPct }
}

export function getScore(branch) {
  const pctAbove = ((branch.gemiddeld - branch.marktbest) / branch.marktbest) * 100
  if (pctAbove === 0)   return 'A'
  if (pctAbove <= 10)   return 'B'
  if (pctAbove <= 20)   return 'C'
  if (pctAbove <= 35)   return 'D'
  return 'E'
}

export const SCORE_CONFIG = {
  A: { color: '#22c55e', label: 'Uitstekend',  description: 'U betaalt al de marktbeste prijs' },
  B: { color: '#84cc16', label: 'Goed',        description: 'U betaalt iets boven de marktprijs' },
  C: { color: '#eab308', label: 'Matig',       description: 'U betaalt beduidend te veel' },
  D: { color: '#f97316', label: 'Hoog',        description: 'Uw premie is fors boven de marktprijs' },
  E: { color: '#ef4444', label: 'Zeer hoog',   description: 'Er is een grote besparing mogelijk' },
}

export function formatCurrency(value) {
  return new Intl.NumberFormat('nl-NL', {
    style: 'currency',
    currency: 'EUR',
    maximumFractionDigits: 0,
  }).format(value)
}

export function formatNumber(value) {
  return new Intl.NumberFormat('nl-NL').format(value)
}
