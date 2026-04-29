import { SCORE_CONFIG, formatCurrency } from '../utils/calculations.js'

function MetricCard({ label, value, valueClass, sub }) {
  return (
    <div className="bg-card-2 rounded-xl p-4 border border-muted">
      <p className="text-xs text-gray-500 uppercase tracking-wide mb-1">{label}</p>
      <p className={`text-2xl font-bold ${valueClass}`}>{value}</p>
      {sub && <p className="text-xs text-gray-500 mt-0.5">{sub}</p>}
    </div>
  )
}

export default function ResultsPanel({ results, branch, score }) {
  const { geschatBesparing, besparingPct, huidigePremie, marktbestePremie } = results
  const scoreConf = SCORE_CONFIG[score]

  return (
    <div className="animate-fade-up">
      {/* Main savings card */}
      <div className="relative bg-card border border-accent/30 rounded-2xl p-6 sm:p-8 mb-4 text-center overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-accent/5 to-transparent pointer-events-none" />
        <p className="text-xs font-semibold text-accent uppercase tracking-widest mb-2">
          Geschatte jaarlijkse besparing
        </p>
        <p className="text-4xl sm:text-5xl font-extrabold text-white mb-2 tracking-tight">
          {formatCurrency(geschatBesparing)}
        </p>
        <p className="text-gray-400 text-sm">
          {besparingPct.toFixed(0)}% minder dan het gemiddelde in uw branche
        </p>
      </div>

      {/* Metric cards row */}
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-4">
        <MetricCard
          label="Branchegemiddelde"
          value={`${branch.gemiddeld}%`}
          valueClass="text-white"
          sub={`≈ ${formatCurrency(huidigePremie)} / jaar`}
        />
        <MetricCard
          label="Marktbeste premie"
          value={`${branch.marktbest}%`}
          valueClass="text-green-400"
          sub="via verzekerverzuim.nl"
        />

        {/* Score badge */}
        <div
          className="col-span-2 sm:col-span-1 rounded-xl p-4 border flex items-center sm:flex-col sm:items-start gap-4 sm:gap-2"
          style={{ borderColor: `${scoreConf.color}33`, background: `${scoreConf.color}0d` }}
        >
          <div
            className="w-12 h-12 shrink-0 rounded-xl flex items-center justify-center text-2xl font-extrabold text-white"
            style={{ background: scoreConf.color }}
          >
            {score}
          </div>
          <div>
            <p className="text-xs text-gray-500 uppercase tracking-wide">Verzuimscore</p>
            <p className="font-bold text-white">{scoreConf.label}</p>
            <p className="text-xs text-gray-400">{scoreConf.description}</p>
          </div>
        </div>
      </div>

      {/* CTA text */}
      <p className="text-center text-sm text-gray-400 mb-6">
        Op basis van <span className="text-white font-medium">{branch.label}</span> — gemiddelden uit de database van 6 verzekeraars
      </p>
    </div>
  )
}
