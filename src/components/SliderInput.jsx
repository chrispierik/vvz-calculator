export default function SliderInput({ label, sublabel, value, onChange, min, max, step, format }) {
  const pct = ((value - min) / (max - min)) * 100
  const trackStyle = {
    background: `linear-gradient(to right, #378ADD ${pct}%, #2a2a2a ${pct}%)`,
  }

  return (
    <div className="mb-6">
      <div className="flex items-start justify-between mb-3">
        <div>
          <label className="block text-sm font-medium text-gray-400">{label}</label>
          {sublabel && <p className="text-xs text-gray-600 mt-0.5">{sublabel}</p>}
        </div>
        <span className="text-lg font-bold text-white ml-4 shrink-0">{format(value)}</span>
      </div>

      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        style={trackStyle}
        className="w-full rounded-full"
      />

      <div className="flex justify-between mt-2">
        <span className="text-xs text-gray-600">{format(min)}</span>
        <span className="text-xs text-gray-600">{format(max)}</span>
      </div>
    </div>
  )
}
