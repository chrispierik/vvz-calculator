import { useState } from 'react'
import { BRANCHES } from './data/branches.js'
import { calculate, getScore, formatCurrency, formatNumber } from './utils/calculations.js'
import ProgressBar from './components/ProgressBar.jsx'
import BrancheSelect from './components/BrancheSelect.jsx'
import SliderInput from './components/SliderInput.jsx'
import ResultsPanel from './components/ResultsPanel.jsx'
import LeadForm from './components/LeadForm.jsx'

function SuccessMessage({ savings }) {
  return (
    <div className="bg-card border border-green-500/30 rounded-2xl p-8 mb-6 text-center animate-fade-up">
      <div className="w-14 h-14 bg-green-500/10 rounded-full flex items-center justify-center mx-auto mb-4">
        <svg className="w-7 h-7 text-green-400" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
        </svg>
      </div>
      <h2 className="text-xl font-bold text-white mb-2">Aanvraag ontvangen!</h2>
      <p className="text-gray-400 text-sm max-w-sm mx-auto">
        U ontvangt binnen 24 uur uw persoonlijke verzuimrapport met offertes van 6 verzekeraars in uw inbox.
      </p>
      <div className="mt-4 inline-block bg-green-500/10 border border-green-500/20 rounded-xl px-5 py-2">
        <p className="text-green-400 text-sm font-medium">
          Potentiële besparing: {formatCurrency(savings)} per jaar
        </p>
      </div>
    </div>
  )
}

export default function App() {
  const [branche, setBranche]               = useState('')
  const [loonsom, setLoonsom]               = useState(800000)
  const [medewerkers, setMedewerkers]       = useState(20)
  const [loonsomTouched, setLoonsomTouched] = useState(false)
  const [medeTouched, setMedeTouched]       = useState(false)
  const [submitted, setSubmitted]           = useState(false)

  const selectedBranch = BRANCHES.find((b) => b.id === branche) || null
  const results        = selectedBranch ? calculate(loonsom, selectedBranch) : null
  const score          = selectedBranch ? getScore(selectedBranch) : null

  const stepsComplete =
    (branche ? 1 : 0) + (loonsomTouched ? 1 : 0) + (medeTouched ? 1 : 0)

  const handleLoonsomChange = (v) => { setLoonsom(v); setLoonsomTouched(true) }
  const handleMedeChange    = (v) => { setMedewerkers(v); setMedeTouched(true) }
  const handleSubmit        = () => setSubmitted(true)

  return (
    <div className="min-h-screen bg-page font-sans text-white">
      {/* Header */}
      <header className="border-b border-muted">
        <div className="max-w-2xl mx-auto px-4 py-4 flex items-center justify-between">
          <div>
            <span className="text-accent font-bold text-base sm:text-lg tracking-tight">
              verzekerverzuim<span className="text-white">.nl</span>
            </span>
            <span className="ml-2 text-xs text-gray-600 hidden sm:inline">
              onderdeel van du Gardijn Verzekeringen
            </span>
          </div>
          <a
            href="https://verzekerverzuim.nl"
            className="text-xs text-gray-500 hover:text-accent transition-colors"
          >
            Meer informatie →
          </a>
        </div>
      </header>

      <main className="max-w-2xl mx-auto px-4 py-8 sm:py-12">
        {/* Hero */}
        <div className="text-center mb-10">
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white mb-3 leading-tight">
            Wat betaal jij eigenlijk<br className="hidden sm:block" />{' '}
            <span className="text-accent">te veel?</span>
          </h1>
          <p className="text-gray-400 text-sm sm:text-base max-w-md mx-auto">
            Beantwoord 3 vragen. Wij schatten je besparing — op basis van gemiddelden uit onze database van 6 verzekeraars.
          </p>
        </div>

        {/* Progress bar */}
        <ProgressBar completed={stepsComplete} />

        {/* Calculator card */}
        <div className="bg-card border border-muted rounded-2xl p-6 sm:p-8 mb-6">
          <BrancheSelect value={branche} onChange={setBranche} />

          <div className="border-t border-muted pt-6">
            <SliderInput
              label="Totale bruto jaarloonsom"
              sublabel="Inclusief alle medewerkers"
              value={loonsom}
              onChange={handleLoonsomChange}
              min={200000}
              max={5000000}
              step={50000}
              format={(v) => formatCurrency(v)}
            />
          </div>

          <div className="border-t border-muted pt-6">
            <SliderInput
              label="Aantal medewerkers"
              value={medewerkers}
              onChange={handleMedeChange}
              min={5}
              max={100}
              step={1}
              format={(v) => `${formatNumber(v)} medewerkers`}
            />
          </div>

          {!branche && (
            <p className="text-center text-xs text-gray-600 mt-2">
              Selecteer een branche om uw besparing te berekenen
            </p>
          )}
        </div>

        {/* Results */}
        {results && !submitted && (
          <ResultsPanel results={results} branch={selectedBranch} score={score} />
        )}

        {/* Lead form or success */}
        {results && !submitted && (
          <LeadForm onSubmit={handleSubmit} />
        )}
        {submitted && results && (
          <SuccessMessage savings={results.geschatBesparing} />
        )}

        {/* Disclaimer */}
        <p className="text-xs text-gray-600 text-center leading-relaxed border-t border-muted pt-6">
          <em>
            Deze berekening is een schatting op basis van gemiddelde marktdata per branche. De werkelijke besparing
            wordt duidelijk na een officiële offerteaanvraag. Aan deze berekening kunnen geen rechten worden ontleend.
          </em>
        </p>
      </main>

      {/* Footer */}
      <footer className="border-t border-muted mt-8">
        <div className="max-w-2xl mx-auto px-4 py-6 flex flex-col sm:flex-row items-center justify-between gap-2 text-xs text-gray-600">
          <span>© {new Date().getFullYear()} du Gardijn Verzekeringen · verzekerverzuim.nl</span>
          <span>AVG-proof · geen cookies zonder toestemming</span>
        </div>
      </footer>
    </div>
  )
}
