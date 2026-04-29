export default function SliderInput({ label, sublabel, value, onChange, min, max, step, format }) {
  const pct = ((value - min) / (max - min)) * 100
  const trackStyle = {
    background: `linear-gradient(to right, #0b349d ${pct}%, #e2e8f0 ${pct}%)`,
  }

  return (
    <div className="mb-6">
      <div className="flex items-start justify-between mb-3">
        <div>
          <label className="block text-sm font-medium text-gray-500">{label}</label>
          {sublabel && <p className="text-xs text-gray-400 mt-0.5">{sublabel}</p>}
        </div>
        <span className="text-lg font-bold text-gray-900 ml-4 shrink-0">{format(value)}</span>
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
        <span className="text-xs text-gray-400">{format(min)}</span>
        <span className="text-xs text-gray-400">{format(max)}</span>
      </div>
    </div>
  )
}
