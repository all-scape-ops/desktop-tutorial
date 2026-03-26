import type { UserPreferences } from '../types';

interface Props {
  prefs: UserPreferences;
  onChange: (prefs: UserPreferences) => void;
}

export default function StepDetails({ prefs, onChange }: Props) {
  const field = (key: keyof UserPreferences) => (e: React.ChangeEvent<HTMLInputElement>) =>
    onChange({ ...prefs, [key]: e.target.value });

  return (
    <div className="flex flex-col items-center gap-8">
      <div className="text-center space-y-3">
        <h2 className="text-3xl font-semibold tracking-tight" style={{ color: '#141414' }}>
          A few more details
        </h2>
        <p className="text-base text-neutral-500 max-w-md">
          This helps us scale the design and ensure products are available near you.
        </p>
      </div>

      <div className="w-full max-w-md space-y-5">
        <div>
          <label className="block text-sm font-medium text-neutral-700 mb-1.5">
            Room size (sq ft)
          </label>
          <input
            type="number"
            min="50"
            placeholder="e.g. 250"
            value={prefs.sqft}
            onChange={field('sqft')}
            className="w-full px-4 py-3 rounded-xl border border-neutral-200 bg-white text-neutral-800 placeholder-neutral-300 focus:outline-none focus:ring-2 focus:ring-neutral-400 transition"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-neutral-700 mb-1.5">City</label>
          <input
            type="text"
            placeholder="e.g. New York"
            value={prefs.city}
            onChange={field('city')}
            className="w-full px-4 py-3 rounded-xl border border-neutral-200 bg-white text-neutral-800 placeholder-neutral-300 focus:outline-none focus:ring-2 focus:ring-neutral-400 transition"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-neutral-700 mb-1.5">Country</label>
          <input
            type="text"
            placeholder="e.g. United States"
            value={prefs.country}
            onChange={field('country')}
            className="w-full px-4 py-3 rounded-xl border border-neutral-200 bg-white text-neutral-800 placeholder-neutral-300 focus:outline-none focus:ring-2 focus:ring-neutral-400 transition"
          />
        </div>
      </div>
    </div>
  );
}
