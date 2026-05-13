import { useState } from 'react'

const VERZUIM_OPTIONS = [
  { label: '0–2%', value: '0-2' },
  { label: '2–4%', value: '2-4' },
  { label: '4–6%', value: '4-6' },
  { label: '6–8%', value: '6-8' },
  { label: '8%+',  value: '8+' },
]

const NAV_STEPS = [
  { id: 1, label: 'Verzuimcijfer' },
  { id: 2, label: 'Loonsom',       preview: '€ 800k' },
  { id: 3, label: 'Wachttijd',     preview: '30 dagen' },
  { id: 4, label: 'Huidige premie',preview: '6.4%' },
  { id: 5, label: 'Uw besparing',  preview: '€ 10,2k' },
  { id: 6, label: 'Uw gegevens' },
]

function StarIcon() {
  return (
    <svg className="w-4 h-4 text-green-400" fill="currentColor" viewBox="0 0 20 20">
      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
    </svg>
  )
}

function Sidebar({ currentStep }) {
  return (
    <aside
      className="w-[380px] min-h-screen relative overflow-hidden flex flex-col px-8 py-8 flex-shrink-0"
      style={{ background: 'linear-gradient(160deg, #1244c8 0%, #0a2e9e 100%)' }}
    >
      {/* Decorative shapes */}
      <div className="absolute bottom-[-50px] right-[-50px] w-60 h-60 border-2 border-white/10 rotate-45 rounded-2xl pointer-events-none" />
      <div className="absolute bottom-[50px] right-[20px] w-36 h-36 border-2 border-white/10 rotate-45 rounded-xl pointer-events-none" />

      {/* Logo */}
      <div className="mb-10">
        <img src="/logo.svg" alt="verzekerverzuim.nl" className="h-10 w-auto" />
      </div>

      {/* Header copy */}
      <div className="mb-8">
        <p className="text-blue-300/80 text-[10px] font-bold tracking-[0.2em] uppercase mb-3">
          Besparing-check
        </p>
        <h2 className="text-white text-[22px] font-bold leading-snug mb-3">
          Ontdek of u te veel betaalt voor uw verzuimverzekering.
        </h2>
        <p className="text-blue-200/70 text-sm leading-relaxed">
          5 korte vragen. Onafhankelijk vergeleken met 6 verzekeraars. Klanten besparen gemiddeld 18%.
        </p>
      </div>

      {/* Step navigation */}
      <nav className="mb-auto">
        {NAV_STEPS.map((step) => {
          const isActive    = step.id === currentStep
          const isCompleted = step.id < currentStep

          return (
            <div
              key={step.id}
              className="flex items-center gap-3 py-3 border-b border-white/10 last:border-b-0"
            >
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0 transition-all ${
                  isActive
                    ? 'bg-white text-[#0b349d] shadow-sm'
                    : isCompleted
                    ? 'bg-white/20 text-white/80'
                    : 'border border-white/25 text-white/40'
                }`}
              >
                {step.id}
              </div>
              <div className="flex items-center justify-between flex-1 min-w-0">
                <span
                  className={`text-sm font-medium truncate ${
                    isActive ? 'text-white' : 'text-white/50'
                  }`}
                >
                  {step.label}
                </span>
                {step.preview && !isActive && (
                  <span className="text-xs text-white/40 ml-3 flex-shrink-0">
                    {step.preview}
                  </span>
                )}
              </div>
            </div>
          )
        })}
      </nav>

      {/* Testimonial */}
      <div className="mt-8 pt-6 border-t border-white/10 relative z-10">
        <div className="flex items-center gap-0.5 mb-2">
          <StarIcon /><StarIcon /><StarIcon /><StarIcon /><StarIcon />
          <span className="text-white/70 text-sm font-semibold ml-1.5">4.8 / 5</span>
          <span className="text-white/40 text-sm ml-1">· 312 reviews</span>
        </div>
        <blockquote className="text-blue-200/80 text-sm italic leading-relaxed">
          "We bespaarden € 8.400 per jaar zonder iets in te leveren op de dekking. Alles via één gesprek."
        </blockquote>
        <p className="text-white/40 text-xs mt-1">— Marieke V., praktijkhouder fysiotherapie</p>
      </div>
    </aside>
  )
}

function VerzuimcijferStep({ value, onChange, onNext }) {
  return (
    <div className="flex flex-col flex-1 px-14 py-14 justify-between">
      <div>
        {/* Step badge */}
        <div className="mb-10">
          <span className="inline-block text-xs font-semibold text-[#378ADD] border border-[#378ADD]/40 bg-[#378ADD]/5 rounded-full px-4 py-1.5 tracking-widest uppercase">
            Vraag 01 / 05
          </span>
        </div>

        {/* Question */}
        <h1 className="text-[32px] font-extrabold text-gray-900 leading-tight mb-3">
          Hoe hoog is het ziekteverzuim in uw praktijk?
        </h1>
        <p className="text-gray-500 text-base leading-relaxed mb-10">
          Kijk naar het gemiddelde van de laatste 3 jaar. Bij twijfel: kies de klasse iets hoger.
        </p>

        {/* Tile pills */}
        <div className="flex gap-3 mb-3">
          {VERZUIM_OPTIONS.map((option) => (
            <button
              key={option.value}
              onClick={() => onChange(option.value)}
              className={`flex-1 py-5 px-2 rounded-xl text-base font-semibold border-2 transition-all text-center ${
                value === option.value
                  ? 'bg-gray-900 border-gray-900 text-white'
                  : 'bg-white border-gray-200 text-gray-700 hover:border-gray-400 hover:bg-gray-50'
              }`}
            >
              {option.label}
            </button>
          ))}
        </div>

        {/* "Weet ik niet" option */}
        <button
          onClick={() => onChange('unknown')}
          className={`w-full py-4 px-6 rounded-xl text-base border-2 transition-all text-center ${
            value === 'unknown'
              ? 'bg-gray-900 border-gray-900 text-white font-semibold'
              : 'bg-white border-gray-200 text-gray-500 hover:border-gray-300 hover:bg-gray-50'
          }`}
        >
          Weet ik niet — gebruik landelijk gemiddelde (4,8%)
        </button>
      </div>

      {/* Navigation */}
      <div className="flex items-center justify-between pt-10">
        <button className="text-gray-400 text-sm hover:text-gray-600 transition-colors">
          ← Terug
        </button>
        <button
          onClick={onNext}
          disabled={!value}
          className="bg-[#2ECC71] hover:bg-[#27AE60] disabled:opacity-40 disabled:cursor-not-allowed text-white text-base font-semibold px-8 py-3 rounded-xl transition-colors"
        >
          Volgende →
        </button>
      </div>
    </div>
  )
}

export default function App() {
  const [currentStep, setCurrentStep]     = useState(1)
  const [verzuimcijfer, setVerzuimcijfer] = useState(null)

  return (
    <div className="min-h-screen flex font-sans">
      <Sidebar currentStep={currentStep} />
      <main className="flex-1 flex flex-col bg-white">
        {currentStep === 1 && (
          <VerzuimcijferStep
            value={verzuimcijfer}
            onChange={setVerzuimcijfer}
            onNext={() => setCurrentStep(2)}
          />
        )}
      </main>
    </div>
  )
}
