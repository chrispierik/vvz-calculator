const STEPS = ['Branche', 'Loonsom', 'Medewerkers']

export default function ProgressBar({ completed }) {
  return (
    <div className="flex items-start justify-center mb-10 select-none">
      {STEPS.map((label, i) => {
        const done   = i < completed
        const active = i === completed
        return (
          <div key={i} className="flex items-start">
            <div className="flex flex-col items-center">
              <div
                className={`w-9 h-9 rounded-full flex items-center justify-center text-sm font-semibold border-2 transition-all duration-300 ${
                  done
                    ? 'bg-accent border-accent text-white'
                    : active
                    ? 'border-accent text-accent bg-transparent'
                    : 'border-muted text-gray-600 bg-transparent'
                }`}
              >
                {done ? (
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                  </svg>
                ) : (
                  i + 1
                )}
              </div>
              <span
                className={`mt-2 text-xs font-medium transition-colors duration-300 ${
                  done || active ? 'text-accent' : 'text-gray-600'
                }`}
              >
                {label}
              </span>
            </div>

            {i < STEPS.length - 1 && (
              <div className="mx-3 mt-4 flex-1 w-16 sm:w-24">
                <div className="h-0.5 w-full bg-muted rounded overflow-hidden">
                  <div
                    className="h-full bg-accent rounded transition-all duration-500"
                    style={{ width: done ? '100%' : '0%' }}
                  />
                </div>
              </div>
            )}
          </div>
        )
      })}
    </div>
  )
}
