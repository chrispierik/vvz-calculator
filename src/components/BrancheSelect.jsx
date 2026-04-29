import { BRANCHES } from '../data/branches.js'

export default function BrancheSelect({ value, onChange }) {
  return (
    <div className="mb-6">
      <label className="block text-sm font-medium text-gray-400 mb-2">
        In welke branche is uw bedrijf actief?
      </label>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className={`w-full bg-card-2 border rounded-xl px-4 py-3.5 text-base font-medium appearance-none cursor-pointer transition-all duration-200 pr-10 ${
          value
            ? 'border-accent text-white'
            : 'border-muted text-gray-500'
        } focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent`}
      >
        <option value="" disabled>Selecteer uw branche</option>
        {BRANCHES.map((b) => (
          <option key={b.id} value={b.id} className="text-white bg-card-2">
            {b.label}
          </option>
        ))}
      </select>
    </div>
  )
}
