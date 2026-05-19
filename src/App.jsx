import { useState } from 'react'
import { calculateFysio, MARKT_GEMIDDELD, WACHTDAGEN_OPTIES } from './utils/calculations.js'

// ── Constants ──────────────────────────────────────────────────────────────────
const VERZUIM_OPTIONS = [
  { label: '0–2%', value: '0-2' },
  { label: '2–4%', value: '2-4' },
  { label: '4–6%', value: '4-6' },
  { label: '6–8%', value: '6-8' },
  { label: '8%+',  value: '8+' },
]

const LOON_CHIPS = [
  { label: '€ 250k', value: 250_000 },
  { label: '€ 500k', value: 500_000 },
  { label: '€ 1M',   value: 1_000_000 },
  { label: '€ 2M',   value: 2_000_000 },
]

const STEP_LABELS        = ['Verzuimcijfer', 'Loonsom', 'Wachttijd', 'Huidige premie', 'Jouw besparing', 'Jouw gegevens']
const MOBILE_STEP_LABELS = ['Verzuim', 'Loonsom', 'Wachttijd', 'Premie', 'Besparing', 'Gegevens']

const WACHTDAGEN_META = {
  10:  { hint: 'Tien werkdagen' },
  20:  { hint: 'Drie weken' },
  30:  { hint: 'Één maand' },
  65:  { hint: 'Twee maanden' },
  130: { hint: 'Vier maanden' },
  261: { hint: 'Negen maanden' },
}

function formatLoonShort(v) {
  if (v >= 1_000_000) return `€ ${(v / 1_000_000).toFixed(v % 1_000_000 === 0 ? 0 : 1)}M`
  return `€ ${Math.round(v / 1_000)}k`
}

function nlNum(v) {
  return Math.round(v).toLocaleString('nl-NL')
}

// ── Logo ───────────────────────────────────────────────────────────────────────
function Logo() {
  return (
    <div className="flex items-center gap-3">
      <svg width="38" height="44" viewBox="0 0 70 72" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M40.2852 64.1741C38.2328 67.7164 33.1005 67.7164 31.0477 64.1741L1.60286 13.3644C-0.449942 9.82215 2.11606 5.39429 6.2217 5.39429H65.1114C69.2172 5.39429 71.783 9.82215 69.7301 13.3644L40.2852 64.1741Z" fill="#015EE1"/>
        <path d="M26.7118 39.9742C24.6512 43.4753 19.5709 43.4753 17.5103 39.9742L1.80171 13.2848C-0.283092 9.74264 2.28086 5.28369 6.40246 5.28369H37.8195C41.9413 5.28369 44.5053 9.74264 42.4204 13.2848L26.7118 39.9742Z" fill="#1040C5"/>
        <path d="M21.8888 48.4551L35.2222 25.2088L27.4444 21.2238L11.4444 7.94019L1.22217 12.368L21.8888 48.4551Z" fill="#1040C5"/>
        <path fillRule="evenodd" clipRule="evenodd" d="M38.4077 23.4377H32.4816V29.3414H26.5557V35.2455H32.4816V41.1492H38.4077V35.2455H44.3334V29.3414H38.4077V23.4377Z" fill="white"/>
      </svg>
      <div className="leading-tight">
        <div className="text-white font-semibold text-[15px]">verzeker</div>
        <div className="text-white font-semibold text-[15px]">verzuim.nl</div>
      </div>
    </div>
  )
}

// ── Mobile Top Bar ─────────────────────────────────────────────────────────────
function MobileTopBar({ step }) {
  if (step > 6) return null
  const label = MOBILE_STEP_LABELS[step - 1] || ''
  return (
    <div
      className="md:hidden sticky top-0 z-20 overflow-hidden"
      style={{ background: 'linear-gradient(180deg, #0A2A8A 0%, #1040C5 100%)' }}
    >
      <svg width="180" height="180" viewBox="0 0 280 280"
        className="absolute top-[-60px] right-[-60px] opacity-[0.08] pointer-events-none" aria-hidden="true">
        <path d="M155 270 L20 30 Q10 10 30 10 L260 10 Q280 10 270 30 L155 270 Z" fill="white" />
      </svg>
      <div className="relative px-5 pt-5 pb-[22px]">
        <div className="flex items-center justify-between mb-[18px]">
          <Logo />
          <div className="text-white text-xs font-semibold tracking-[.02em] px-3 py-[5px] rounded-full"
            style={{ background: 'rgba(255,255,255,0.12)' }}>
            Stap {step} / 6
          </div>
        </div>
        <div className="flex items-center gap-1.5">
          {MOBILE_STEP_LABELS.map((_, i) => (
            <div key={i} className="flex-1 h-1 rounded-sm transition-colors duration-300"
              style={{ background: i + 1 <= step ? '#1ABC9C' : 'rgba(255,255,255,0.18)' }} />
          ))}
        </div>
        <div className="text-white/85 text-[13px] mt-2.5">{label}</div>
      </div>
    </div>
  )
}

// ── Sidebar ────────────────────────────────────────────────────────────────────
function Sidebar({ step, verzuim, loon, wachttijd, premiePct }) {
  const verzuimLabel = { '0-2': '0–2%', '2-4': '2–4%', '4-6': '4–6%', '6-8': '6–8%', '8+': '8%+', unk: 'gem.' }
  const summaries = {
    1: verzuim ? verzuimLabel[verzuim] ?? null : null,
    2: formatLoonShort(loon),
    3: `${wachttijd} d.`,
    4: `${premiePct.toFixed(1)}%`,
  }

  return (
    <aside
      className="hidden md:flex w-[340px] min-h-screen relative overflow-hidden flex-col px-7 py-8 flex-shrink-0"
      style={{ background: 'linear-gradient(180deg, #0A2A8A 0%, #1040C5 100%)' }}
    >
      <div className="absolute bottom-[-50px] right-[-50px] w-56 h-56 border-2 border-white/10 rotate-45 rounded-2xl pointer-events-none" />
      <div className="absolute bottom-[60px] right-[30px] w-32 h-32 border-2 border-white/10 rotate-45 rounded-xl pointer-events-none" />

      <div className="mb-10"><Logo /></div>

      <div className="mb-8">
        <p className="text-blue-300/70 text-[10px] font-bold tracking-[.2em] uppercase mb-3">Jouw besparingscheck</p>
        <h2 className="text-white text-[22px] font-bold leading-snug mb-3">
          Betaal jij te veel voor je verzuimverzekering?
        </h2>
        <p className="text-blue-200/70 text-sm leading-relaxed">
          5 vragen. Vergeleken met 6 verzekeraars. Klanten besparen gemiddeld 18%.
        </p>
      </div>

      <nav className="mb-auto">
        {STEP_LABELS.map((label, i) => {
          const idx      = i + 1
          const isDone   = idx < step
          const isActive = idx === step || (step === 7 && idx === 6)
          return (
            <div key={idx} className="flex items-center gap-3 py-3 border-b border-white/10 last:border-b-0">
              <div className={`w-7 h-7 rounded-full flex items-center justify-center text-[13px] font-bold flex-shrink-0 ${
                isDone   ? 'bg-[#1ABC9C] text-white' :
                isActive ? 'bg-white text-[#1040C5]' :
                           'border border-white/30 text-white/40'
              }`}>
                {isDone ? '✓' : idx}
              </div>
              <div className="flex items-center justify-between flex-1 min-w-0">
                <span className={`text-sm truncate ${
                  isActive ? 'text-white font-semibold' : isDone ? 'text-white/80 font-medium' : 'text-white/40'
                }`}>{label}</span>
                {isDone && summaries[idx] && (
                  <span className="text-xs text-white/60 ml-2 flex-shrink-0 tabular-nums">{summaries[idx]}</span>
                )}
              </div>
            </div>
          )
        })}
      </nav>

      <div className="mt-8 pt-6 border-t border-white/15">
        <div className="flex items-center gap-1 mb-2">
          {[...Array(5)].map((_, i) => (
            <svg key={i} className="w-3.5 h-3.5 text-[#1ABC9C]" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
          ))}
          <span className="text-white/70 text-sm font-semibold ml-1">4,8 / 5</span>
          <span className="text-white/40 text-xs ml-1">· 312 reviews</span>
        </div>
        <blockquote className="text-blue-200/80 text-sm italic leading-relaxed">
          "We bespaarden € 8.400 per jaar zonder iets in te leveren op de dekking. Alles via één gesprek."
        </blockquote>
        <p className="text-white/40 text-xs mt-1">— Marieke V., praktijkhouder fysiotherapie</p>
      </div>
    </aside>
  )
}

// ── Shared: question header ────────────────────────────────────────────────────
function QHead({ num, title, helper, result = false }) {
  return (
    <div className="mb-6 md:mb-8">
      <span className={`inline-block text-[10px] md:text-[11px] font-semibold rounded-md px-2.5 py-1 tracking-[.14em] uppercase mb-3 ${
        result ? 'text-[#0E7C66] bg-[#D6F2EB]' : 'text-[#015EE1] bg-[#E6EEFB]'
      }`}>
        {result ? '✓ Resultaat' : `Vraag ${String(num).padStart(2, '0')} / 05`}
      </span>
      <h1 className="text-[22px] md:text-[34px] font-bold text-[#0B1530] leading-[1.2] md:leading-[1.15] tracking-tight mb-2 md:mb-3"
        dangerouslySetInnerHTML={{ __html: title }} />
      {helper && (
        <p className="text-[#5A6488] text-[14px] md:text-[15px] leading-relaxed"
          dangerouslySetInnerHTML={{ __html: helper }} />
      )}
    </div>
  )
}

// ── Shared: navigation ─────────────────────────────────────────────────────────
function Nav({ onBack, onNext, nextLabel = 'Volgende →', nextDisabled = false, hideBack = false }) {
  return (
    <>
      {/* Desktop nav — inline */}
      <div className="hidden md:flex items-center justify-between pt-10 mt-auto">
        {!hideBack
          ? <button onClick={onBack} className="text-[#5A6488] text-sm font-medium hover:text-[#0B1530] transition-colors">← Terug</button>
          : <div />}
        <button
          onClick={onNext}
          disabled={nextDisabled}
          className="bg-[#1ABC9C] hover:bg-[#16A085] disabled:opacity-40 disabled:cursor-not-allowed text-white text-[15px] font-bold px-8 py-3.5 rounded-xl transition-colors"
          style={{ boxShadow: '0 12px 28px -10px rgba(26,188,156,.5)' }}
        >
          {nextLabel}
        </button>
      </div>

      {/* Mobile nav — sticky bottom */}
      <div
        className="md:hidden sticky bottom-0 z-10 -mx-5 border-t border-[#EBEEF5] px-5 pt-3.5 pb-7 flex items-center gap-2.5"
        style={{ background: 'rgba(255,255,255,0.97)', backdropFilter: 'blur(12px)' }}
      >
        {!hideBack ? (
          <button
            onClick={onBack}
            className="w-12 h-12 rounded-xl bg-[#F5F7FB] border border-[#EBEEF5] text-[#2A3454] text-base flex-shrink-0 flex items-center justify-center"
          >←</button>
        ) : (
          <div className="w-12 flex-shrink-0" />
        )}
        <button
          onClick={onNext}
          disabled={nextDisabled}
          className="flex-1 text-[15px] font-bold py-3.5 rounded-xl flex items-center justify-center gap-2 transition-colors disabled:cursor-not-allowed"
          style={{
            background: nextDisabled ? '#EBEEF5' : '#1ABC9C',
            color: nextDisabled ? '#8089A8' : '#fff',
            boxShadow: nextDisabled ? 'none' : '0 12px 28px -10px rgba(26,188,156,.5)',
          }}
        >
          {nextLabel}
        </button>
      </div>
    </>
  )
}

// ── Step 1: Verzuimcijfer ──────────────────────────────────────────────────────
function Step1({ value, onChange, onNext }) {
  return (
    <div className="flex flex-col md:h-full">
      <QHead num={1}
        title="Hoe hoog is het ziekteverzuim in jouw praktijk?"
        helper="Neem het gemiddelde van de afgelopen 3 jaar. Twijfel je? Kies de klasse iets hoger."
      />

      <div className="bg-[#F5F7FB] rounded-2xl p-1.5 flex gap-1 mb-3">
        {VERZUIM_OPTIONS.map((opt) => (
          <button key={opt.value} onClick={() => onChange(opt.value)}
            className={`flex-1 py-3 md:py-3.5 rounded-xl text-[13px] md:text-[15px] transition-all ${
              value === opt.value
                ? 'bg-white text-[#0B1530] font-bold shadow-sm'
                : 'text-[#5A6488] font-medium hover:text-[#0B1530]'
            }`}>
            {opt.label}
          </button>
        ))}
      </div>

      <button onClick={() => onChange('unk')}
        className={`w-full py-3.5 md:py-4 px-6 rounded-2xl text-[13px] md:text-[15px] border-2 transition-all ${
          value === 'unk'
            ? 'bg-white border-[#0B1530] text-[#0B1530] font-semibold'
            : 'bg-white border-dashed border-[#DCE0EC] text-[#8089A8] hover:border-[#5A6488] hover:text-[#5A6488]'
        }`}>
        Weet ik niet, gebruik het landelijk gemiddelde (4,8%)
      </button>

      <Nav hideBack onNext={onNext} nextDisabled={!value} />
    </div>
  )
}

// ── Step 2: Loonsom ────────────────────────────────────────────────────────────
function Step2({ value, onChange, onBack, onNext }) {
  const [customLoon, setCustomLoon] = useState('')
  const sliderValue = Math.min(value, 3_000_000)
  const pct = ((sliderValue - 100_000) / 2_900_000) * 100
  return (
    <div className="flex flex-col md:h-full">
      <QHead num={2}
        title="Wat is jouw totale loonsom per jaar?"
        helper="Tel alle bruto salarissen van je medewerkers op (vóór belasting). Dit is de basis waarover jouw premie wordt berekend."
      />

      <div className="text-center mb-2">
        <p className="text-[11px] font-mono text-[#8089A8] uppercase tracking-[.1em]">Loonsom per jaar</p>
        <p className="text-[40px] md:text-[60px] font-bold text-[#0B1530] leading-none tracking-tight tabular-nums mt-2">
          <span className="text-[#8089A8]">€&nbsp;</span>{nlNum(value)}
        </p>
      </div>

      <div className="mt-5 md:mt-6">
        <input type="range" min={100_000} max={3_000_000} step={10_000} value={sliderValue}
          onChange={(e) => {
            const v = Number(e.target.value)
            if (v < 3_000_000) setCustomLoon('')
            onChange(v)
          }}
          style={{ background: `linear-gradient(to right, #015EE1 ${pct}%, #E2E8F0 ${pct}%)` }}
          className="w-full rounded-full"
        />
        <div className="flex justify-between mt-1.5">
          <span className="text-xs text-[#8089A8]">€ 100k</span>
          <span className="text-xs text-[#8089A8]">€ 3M</span>
        </div>
      </div>

      {sliderValue === 3_000_000 && (
        <div className="mt-4 p-4 rounded-2xl bg-[#F4F7FD] border border-[#DCE0EC]">
          <p className="text-[13px] text-[#2A3454] mb-2">
            Heb je een loonzone hoger dan 3 miljoen? Vul dan hier je exacte loonzone in.
          </p>
          <div className="relative">
            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-[#8089A8] font-medium text-[14px]">€</span>
            <input
              type="number"
              min={3_000_001}
              placeholder="Bijv. 4500000"
              value={customLoon}
              onChange={(e) => {
                setCustomLoon(e.target.value)
                const num = Number(e.target.value)
                if (num > 3_000_000) onChange(num)
              }}
              className="w-full pl-7 pr-4 py-2.5 rounded-xl border border-[#DCE0EC] bg-white text-[#0B1530] text-[15px] font-medium focus:outline-none focus:border-[#015EE1] focus:ring-2 focus:ring-[#015EE1]/20"
            />
          </div>
        </div>
      )}

      <div className="flex flex-wrap gap-2 mt-4 md:mt-5">
        {LOON_CHIPS.map((chip) => (
          <button key={chip.value} onClick={() => { setCustomLoon(''); onChange(chip.value) }}
            className={`px-4 py-2 rounded-full text-[13px] font-medium border transition-all ${
              value === chip.value
                ? 'bg-[#0B1530] text-white border-[#0B1530]'
                : 'bg-white text-[#2A3454] border-[#DCE0EC] hover:bg-[#0B1530] hover:text-white hover:border-[#0B1530]'
            }`}>
            {chip.label}
          </button>
        ))}
      </div>

      <Nav onBack={onBack} onNext={onNext} />
    </div>
  )
}

// ── Step 3: Wachttijd ──────────────────────────────────────────────────────────
function Step3({ value, onChange, onBack, onNext }) {
  return (
    <div className="flex flex-col md:h-full">
      <QHead num={3}
        title="Hoeveel dagen wachttijd heb jij?"
        helper='Dit is de periode dat jij zelf het loon doorbetaalt voordat de verzekering uitkeert. Op je polisblad staat dit als <strong style="color:#0B1530">"eigen risico"</strong>. Hoe langer, hoe lager je premie.'
      />

      {/* Desktop: big number grid */}
      <div className="hidden md:grid grid-cols-3 gap-3 sm:grid-cols-6">
        {WACHTDAGEN_OPTIES.map((d) => (
          <button key={d} onClick={() => onChange(d)}
            className={`py-5 rounded-2xl text-[26px] font-bold border-2 transition-all ${
              value === d
                ? 'border-[#015EE1] bg-[#F4F7FD] text-[#1040C5]'
                : 'border-[#EBEEF5] bg-white text-[#0B1530] hover:border-[#DCE0EC] hover:bg-[#F5F7FB]'
            }`}>
            {d}
          </button>
        ))}
      </div>
      <p className="hidden md:block text-[13px] text-[#8089A8] italic mt-3">
        Staat op je polisblad als "eigen risico periode"
      </p>

      {/* Mobile: vertical radio list */}
      <div className="md:hidden flex flex-col gap-2">
        {WACHTDAGEN_OPTIES.map((d) => (
          <button key={d} onClick={() => onChange(d)}
            className={`flex items-center justify-between p-4 rounded-xl border-[1.5px] text-left transition-all ${
              value === d
                ? 'border-[#015EE1] bg-[#F4F7FD]'
                : 'border-[#EBEEF5] bg-white'
            }`}>
            <div>
              <div className="text-[16px] font-semibold text-[#0B1530]">{d} dagen</div>
              <div className="text-[12px] text-[#8089A8] mt-0.5">{WACHTDAGEN_META[d]?.hint}</div>
            </div>
            <div className={`w-[22px] h-[22px] rounded-full border-[1.5px] flex items-center justify-center flex-shrink-0 text-xs font-bold transition-all ${
              value === d
                ? 'bg-[#1ABC9C] border-transparent text-white'
                : 'border-[#B7BED4] bg-transparent text-transparent'
            }`}>
              ✓
            </div>
          </button>
        ))}
      </div>

      <Nav onBack={onBack} onNext={onNext} />
    </div>
  )
}

// ── Step 4: Huidige premie ─────────────────────────────────────────────────────
function Step4({ value, onChange, jaarpremie, onJaarpremie, loon, onBack, onNext }) {
  const above = value > 3
  const diff  = above ? Math.round(((value - 3) / 3) * 100) : 0
  const pct   = (value / 12) * 100
  const euros = Math.round(loon * (value / 100))

  return (
    <div className="flex flex-col md:h-full">
      <QHead num={4}
        title="Welk premiepercentage betaal jij nu?"
        helper={`Het marktgemiddelde voor fysiotherapeuten is <strong style="color:#0B1530">${MARKT_GEMIDDELD}%</strong>. Sleep de slider of vul je exacte jaarpremie in.`}
      />

      <div className="text-center mb-2">
        <p className={`text-[56px] md:text-[80px] font-bold leading-none tracking-tight tabular-nums ${above ? 'text-[#D14D2C]' : 'text-[#0B1530]'}`}>
          {value.toFixed(1)}<span className="text-[32px] md:text-[44px] text-[#8089A8]">%</span>
        </p>
        <span className={`inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-[12px] md:text-[13px] font-semibold mt-2 md:mt-3 ${
          above ? 'bg-[#FFF1EB] text-[#A8401A]' : 'bg-[#D6F2EB] text-[#0E7C66]'
        }`}>
          {above ? `↑ ${diff}% boven het marktgemiddelde` : '↓ Op of onder het marktgemiddelde'}
        </span>
      </div>

      <div className="mt-5 md:mt-6">
        <input type="range" min={0} max={12} step={0.1} value={value}
          onChange={(e) => onChange(Number(e.target.value))}
          style={{ background: `linear-gradient(to right, ${above ? '#D14D2C' : '#015EE1'} ${pct}%, #E2E8F0 ${pct}%)` }}
          className="w-full rounded-full"
        />
        <div className="flex justify-between mt-1.5">
          <span className="text-xs text-[#8089A8]">0%</span>
          <span className="text-xs text-[#8089A8]">12%</span>
        </div>
      </div>

      <div className="mt-4 md:mt-5 p-4 bg-[#F5F7FB] rounded-2xl flex items-center justify-between">
        <div>
          <p className="text-[11px] text-[#5A6488] uppercase tracking-[.08em]">Komt neer op</p>
          <p className="text-[18px] md:text-[22px] font-bold text-[#0B1530] mt-1 tabular-nums">€ {nlNum(euros)} / jaar</p>
        </div>
      </div>

      <div className="mt-4">
        <p className="text-[12px] md:text-[13px] text-[#5A6488] mb-1.5">
          Of vul je exacte jaarpremie in{' '}
          <span className="text-[10px] bg-[#EBEEF5] px-1.5 py-0.5 rounded font-semibold tracking-wide">OPTIONEEL</span>
        </p>
        <input type="number" min={0} max={999_999} step={500} value={jaarpremie}
          onChange={(e) => onJaarpremie(e.target.value)}
          placeholder="bijv. 12.500"
          className="w-full bg-white border-[1.5px] border-[#DCE0EC] rounded-xl px-4 py-3 md:py-3.5 text-[15px] text-[#0B1530] placeholder-[#8089A8] focus:outline-none focus:border-[#1040C5] transition-all"
        />
      </div>

      <Nav onBack={onBack} onNext={onNext} nextLabel="Bereken mijn besparing →" />
    </div>
  )
}

// ── Step 5: Resultaat ──────────────────────────────────────────────────────────
function Step5({ results, effPct, onBack, onNext }) {
  const { ourRate, onzePremie, huidigePremie, besparing, besparingPct } = results
  const pctShow = Math.round(besparingPct)

  return (
    <div className="flex flex-col md:h-full">
      <QHead result
        title={`Je bespaart naar verwachting <span style="color:#1040C5">${pctShow}%</span> op je verzuimverzekering.`}
      />

      <div className="relative rounded-2xl md:rounded-3xl p-6 md:p-8 mb-3 overflow-hidden"
        style={{ background: 'linear-gradient(135deg, #1040C5 0%, #015EE1 100%)', boxShadow: '0 16px 40px -12px rgba(1,94,225,.35)' }}>
        <div className="absolute top-[-80px] right-[-80px] w-64 h-64 rounded-full pointer-events-none"
          style={{ background: 'radial-gradient(circle, rgba(26,188,156,.4), transparent 70%)' }} />
        <div className="relative z-10">
          <p className="text-[10px] md:text-[11px] font-mono text-white/70 uppercase tracking-[.14em]">Geschatte jaarbesparing</p>
          <p className="text-[48px] md:text-[68px] font-bold text-white leading-none tracking-tight tabular-nums mt-1.5">
            <span className="text-white/60 text-[28px] md:text-[42px]">€&nbsp;</span>{nlNum(besparing)}
          </p>
          <span className="inline-flex items-center gap-2 bg-[#1ABC9C] text-white text-[12px] md:text-[13px] font-bold px-4 py-1.5 rounded-full mt-3">
            ↓ {pctShow}% lager dan je huidige premie
          </span>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3 mb-4 md:mb-5">
        <div className="bg-[#F5F7FB] rounded-xl md:rounded-2xl p-4 md:p-5">
          <p className="text-[10px] md:text-[11px] font-semibold uppercase tracking-[.08em] text-[#5A6488]">Jouw huidige premie</p>
          <p className="text-[20px] md:text-[26px] font-bold text-[#2A3454] mt-1.5 tabular-nums">€ {nlNum(huidigePremie)}</p>
          <p className="text-xs text-[#8089A8] mt-1">per jaar · {effPct.toFixed(1)}%</p>
        </div>
        <div className="bg-[#F4F7FD] rounded-xl md:rounded-2xl p-4 md:p-5">
          <p className="text-[10px] md:text-[11px] font-semibold uppercase tracking-[.08em] text-[#5A6488]">Jouw nieuwe premie via ons</p>
          <p className="text-[20px] md:text-[26px] font-bold text-[#1040C5] mt-1.5 tabular-nums">€ {nlNum(onzePremie)}</p>
          <p className="text-xs text-[#8089A8] mt-1">per jaar · {ourRate.toFixed(3)}%</p>
        </div>
      </div>

      <Nav onBack={onBack} onNext={onNext} nextLabel="Claim deze besparing →" />
    </div>
  )
}

// ── Step 6: Gegevens ───────────────────────────────────────────────────────────
function Step6({ besparing, form, onChange, onBack, onSubmit,
                 verzuim, loon, wachttijd, premiePct, jaarpremie, effPct, results }) {
  const [loading, setLoading] = useState(false)
  const set = (key) => (e) => onChange({ ...form, [key]: e.target.value })

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      await fetch('https://n8n.dugardijn.nl/webhook/5deca357-d9c0-454e-b886-109cb916a98d', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          stap1_verzuimpercentage: verzuim ? `${verzuim}%` : 'onbekend',
          stap2_loonsom_euro: loon,
          stap3_wachtdagen: wachttijd,
          stap4_premiepercentage_pct: premiePct,
          stap4_jaarpremie_euro: jaarpremie && Number(jaarpremie) > 0 ? Number(jaarpremie) : null,
          berekening_effectief_premiepercentage_pct: effPct,
          berekening_huidige_premie_euro: Math.round(results?.huidigePremie ?? 0),
          berekening_onze_premie_euro: Math.round(results?.onzePremie ?? 0),
          berekening_ons_premiepercentage_pct: results?.ourRate ?? 0,
          berekening_besparing_euro: Math.round(results?.besparing ?? 0),
          berekening_besparing_pct: Math.round(results?.besparingPct ?? 0),
          bedrijfsnaam: form.bedrijf,
          email: form.email,
          telefoonnummer: form.tel,
        }),
      })
    } catch (_) {}
    onSubmit()
    setLoading(false)
  }

  const isValid = form.bedrijf && form.email && form.tel

  return (
    <div className="flex flex-col md:h-full">
      <QHead num={5}
        title="Naar wie sturen we jouw besparing?"
        helper="Persoonlijk overzicht in je inbox binnen 1 minuut. Geen verkooppraatjes — eerlijke vergelijking met 6 verzekeraars."
      />

      {besparing > 0 && (
        <div className="flex items-center justify-between gap-4 p-3.5 md:p-4 rounded-xl md:rounded-2xl bg-[#EBF8F4] border border-[#1ABC9C] mb-5 md:mb-6">
          <div>
            <p className="text-[9px] md:text-[10px] font-mono font-semibold uppercase tracking-[.12em] text-[#0E7C66]">Jouw besparing staat klaar</p>
            <p className="text-[14px] md:text-[15px] font-semibold text-[#0B1530] mt-1">
              Jouw besparing van <span className="text-[#1040C5] tabular-nums">€ {nlNum(besparing)}</span> per jaar
            </p>
          </div>
          <div className="w-8 h-8 md:w-9 md:h-9 rounded-full bg-[#1ABC9C] flex items-center justify-center text-white text-sm flex-shrink-0">✉</div>
        </div>
      )}

      <form onSubmit={handleSubmit} className="flex flex-col flex-1">
        <div className="space-y-3.5 md:space-y-4 flex-1">
          {[
            { key: 'bedrijf', label: 'Bedrijfsnaam',   placeholder: 'Fysiotherapie Voorbeeld B.V.', required: true },
            { key: 'email',   label: 'E-mailadres',    placeholder: 'naam@bedrijf.nl', type: 'email', required: true },
            { key: 'tel',     label: 'Telefoonnummer', placeholder: '06 12 34 56 78',  type: 'tel',   required: true },
          ].map(({ key, label, placeholder, type = 'text', required }) => (
            <div key={key}>
              <label className="block text-[12px] md:text-[13px] font-semibold text-[#2A3454] mb-1.5">
                {label} {required && <span className="text-[#1ABC9C]">*</span>}
              </label>
              <input type={type} value={form[key]} onChange={set(key)} required={required} placeholder={placeholder}
                className="w-full bg-white border-[1.5px] border-[#DCE0EC] rounded-xl px-4 py-3 md:py-3.5 text-[15px] text-[#0B1530] placeholder-[#8089A8] focus:outline-none focus:border-[#1040C5] transition-all"
              />
            </div>
          ))}
          <p className="text-xs text-[#8089A8]">🔒 Versleuteld verzonden · we delen niets met derden</p>
        </div>

        {/* Desktop submit */}
        <div className="hidden md:block pt-6">
          <button type="submit" disabled={loading}
            className="w-full bg-[#1ABC9C] hover:bg-[#16A085] disabled:opacity-60 text-white text-[15px] font-bold py-4 rounded-xl transition-colors flex items-center justify-center gap-2"
            style={{ boxShadow: '0 12px 28px -10px rgba(26,188,156,.5)' }}>
            {loading ? (
              <>
                <svg className="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
                </svg>
                Bezig...
              </>
            ) : 'Stuur naar mij →'}
          </button>
          <button type="button" onClick={onBack}
            className="w-full mt-3 text-[#5A6488] text-sm font-medium hover:text-[#0B1530] transition-colors py-2">
            ← Terug naar jouw besparing
          </button>
        </div>

        {/* Mobile submit — sticky bottom */}
        <div
          className="md:hidden sticky bottom-0 z-10 -mx-5 border-t border-[#EBEEF5] px-5 pt-3.5 pb-7 flex items-center gap-2.5"
          style={{ background: 'rgba(255,255,255,0.97)', backdropFilter: 'blur(12px)' }}
        >
          <button type="button" onClick={onBack}
            className="w-12 h-12 rounded-xl bg-[#F5F7FB] border border-[#EBEEF5] text-[#2A3454] text-base flex-shrink-0 flex items-center justify-center">
            ←
          </button>
          <button type="submit" disabled={loading || !isValid}
            className="flex-1 text-[15px] font-bold py-3.5 rounded-xl flex items-center justify-center gap-2 transition-colors disabled:cursor-not-allowed"
            style={{
              background: loading || !isValid ? '#EBEEF5' : '#1ABC9C',
              color: loading || !isValid ? '#8089A8' : '#fff',
              boxShadow: loading || !isValid ? 'none' : '0 12px 28px -10px rgba(26,188,156,.5)',
            }}>
            {loading ? 'Bezig...' : 'Stuur naar mij →'}
          </button>
        </div>
      </form>
    </div>
  )
}

// ── Step 7: Bedankt ────────────────────────────────────────────────────────────
function Step7({ bedrijf, email, besparing, onRestart }) {
  return (
    <div className="flex flex-col pt-4 md:pt-0 md:h-full md:justify-center">
      <div className="w-14 h-14 rounded-full bg-[#1ABC9C] flex items-center justify-center text-white text-3xl font-bold mb-5 md:mb-6">✓</div>
      <h1 className="text-[26px] md:text-[34px] font-bold text-[#0B1530] leading-[1.15] tracking-tight mb-3 md:mb-4">
        Goed gedaan{bedrijf ? `, ${bedrijf}` : ''}!
      </h1>
      <p className="text-[#5A6488] text-[14px] md:text-[15px] leading-relaxed mb-7 md:mb-8">
        Jouw persoonlijke overzicht — met een verwachte besparing van{' '}
        <strong className="text-[#0B1530]">€ {nlNum(besparing)} per jaar</strong> — is onderweg naar{' '}
        <strong className="text-[#0B1530]">{email || 'je inbox'}</strong>.
        Een adviseur belt je binnen 1 werkdag.
      </p>
      <button onClick={onRestart}
        className="self-start bg-[#F5F7FB] hover:bg-[#EBEEF5] text-[#0B1530] text-[14px] font-medium px-6 py-3 rounded-xl transition-colors">
        Nieuwe berekening
      </button>
    </div>
  )
}

// ── App ────────────────────────────────────────────────────────────────────────
export default function App() {
  const [step, setStep]           = useState(1)
  const [verzuim, setVerzuim]     = useState('unk')
  const [loon, setLoon]           = useState(800_000)
  const [wachttijd, setWachttijd] = useState(30)
  const [premiePct, setPremiePct] = useState(MARKT_GEMIDDELD)
  const [jaarpremie, setJaarpremie] = useState('')
  const [form, setForm]           = useState({ bedrijf: '', email: '', tel: '' })
  const [results, setResults]     = useState(null)
  const [effPct, setEffPct]       = useState(MARKT_GEMIDDELD)

  const next = () => setStep((s) => s + 1)
  const back = () => setStep((s) => s - 1)

  const computeResults = () => {
    const ep = jaarpremie && Number(jaarpremie) > 0 && loon > 0
      ? (Number(jaarpremie) / loon) * 100
      : premiePct
    setEffPct(ep)
    setResults(calculateFysio(loon, wachttijd, ep))
    next()
  }

  const restart = () => {
    setStep(1); setVerzuim(null); setLoon(800_000); setWachttijd(30)
    setPremiePct(MARKT_GEMIDDELD); setJaarpremie(''); setForm({ bedrijf: '', email: '', tel: '' })
    setResults(null); setEffPct(MARKT_GEMIDDELD)
  }

  return (
    <div className="min-h-screen flex font-sans bg-[#FAFBFE]">
      {/* Desktop sidebar — hidden on mobile */}
      <Sidebar step={step} verzuim={verzuim} loon={loon} wachttijd={wachttijd} premiePct={premiePct} />

      {/* Content area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Mobile top bar */}
        <MobileTopBar step={step} />

        {/* Main */}
        <main className="flex-1 flex flex-col px-5 py-5 md:px-14 md:py-14" style={{ maxWidth: 760 }}>
          {step === 1 && <Step1 value={verzuim} onChange={setVerzuim} onNext={next} />}
          {step === 2 && <Step2 value={loon} onChange={setLoon} onBack={back} onNext={next} />}
          {step === 3 && <Step3 value={wachttijd} onChange={setWachttijd} onBack={back} onNext={next} />}
          {step === 4 && (
            <Step4 value={premiePct} onChange={setPremiePct}
              jaarpremie={jaarpremie} onJaarpremie={setJaarpremie}
              loon={loon} onBack={back} onNext={computeResults} />
          )}
          {step === 5 && results && (
            <Step5 results={results} effPct={effPct} onBack={back} onNext={next} />
          )}
          {step === 6 && (
            <Step6 besparing={results?.besparing ?? 0}
              form={form} onChange={setForm} onBack={back} onSubmit={next}
              verzuim={verzuim} loon={loon} wachttijd={wachttijd}
              premiePct={premiePct} jaarpremie={jaarpremie}
              effPct={effPct} results={results} />
          )}
          {step === 7 && (
            <Step7 bedrijf={form.bedrijf} email={form.email}
              besparing={results?.besparing ?? 0} onRestart={restart} />
          )}

        </main>
      </div>
    </div>
  )
}
