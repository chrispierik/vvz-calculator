import { useState } from 'react'

function Field({ label, id, type = 'text', value, onChange, required, placeholder }) {
  return (
    <div>
      <label htmlFor={id} className="block text-sm font-medium text-gray-400 mb-1.5">
        {label} {required && <span className="text-accent">*</span>}
      </label>
      <input
        id={id}
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        required={required}
        placeholder={placeholder}
        className="w-full bg-card-2 border border-muted rounded-xl px-4 py-3 text-white placeholder-gray-600 text-sm transition-all duration-200 focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent"
      />
    </div>
  )
}

export default function LeadForm({ onSubmit }) {
  const [form, setForm] = useState({ naam: '', bedrijf: '', email: '', telefoon: '' })
  const [loading, setLoading] = useState(false)

  const set = (key) => (val) => setForm((f) => ({ ...f, [key]: val }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    await new Promise((r) => setTimeout(r, 800)) // Replace with actual API call
    onSubmit(form)
    setLoading(false)
  }

  return (
    <div className="bg-card border border-muted rounded-2xl p-6 sm:p-8 mb-6 animate-fade-up">
      <div className="mb-6">
        <h2 className="text-xl font-bold text-white mb-1">
          Vraag gratis offertes aan bij 6 verzekeraars
        </h2>
        <p className="text-gray-400 text-sm">
          Binnen 24 uur de beste offertes in uw inbox — zonder verdere verplichtingen.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <Field
            label="Naam" id="naam"
            value={form.naam} onChange={set('naam')}
            required placeholder="Jan de Vries"
          />
          <Field
            label="Bedrijfsnaam" id="bedrijf"
            value={form.bedrijf} onChange={set('bedrijf')}
            required placeholder="Mijn Bedrijf B.V."
          />
        </div>
        <Field
          label="E-mailadres" id="email" type="email"
          value={form.email} onChange={set('email')}
          required placeholder="jan@mijnbedrijf.nl"
        />
        <Field
          label="Telefoonnummer" id="telefoon" type="tel"
          value={form.telefoon} onChange={set('telefoon')}
          placeholder="06 12 34 56 78"
        />

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-accent hover:bg-accent-hover disabled:opacity-60 text-white font-semibold py-3.5 px-6 rounded-xl transition-all duration-200 text-sm sm:text-base flex items-center justify-center gap-2 mt-2"
        >
          {loading ? (
            <>
              <svg className="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
              </svg>
              Bezig...
            </>
          ) : (
            <>
              Ontvang mijn gratis offertes
              <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </>
          )}
        </button>

        <p className="text-xs text-gray-600 text-center">
          Geen spam. U ontvangt het verzuimrapport + offertes per e-mail.
        </p>
      </form>
    </div>
  )
}
