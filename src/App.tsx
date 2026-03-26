import { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { Palette, ChevronRight, ArrowLeft } from 'lucide-react';

import StepUpload from './components/StepUpload';
import StepStyle from './components/StepStyle';
import StepDetails from './components/StepDetails';
import StepResults from './components/StepResults';

import { BUDGET_TIERS } from './lib/constants';
import { generateDesigns } from './lib/gemini';
import type { StyleOption, DesignResult, UserPreferences } from './types';

type Step = 'upload' | 'style' | 'details' | 'results';
const STEPS: Step[] = ['upload', 'style', 'details', 'results'];
const STEP_LABELS: Record<Step, string> = {
  upload: 'Upload',
  style: 'Style',
  details: 'Details',
  results: 'Results',
};

export default function App() {
  const [step, setStep] = useState<Step>('upload');
  const [imageBase64, setImageBase64] = useState('');
  const [imageMime, setImageMime] = useState('image/jpeg');
  const [imagePreview, setImagePreview] = useState('');
  const [selectedStyle, setSelectedStyle] = useState<StyleOption | null>(null);
  const [prefs, setPrefs] = useState<UserPreferences>({ sqft: '', city: '', country: '' });
  const [results, setResults] = useState<DesignResult[]>([]);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState('');

  const stepIndex = STEPS.indexOf(step);

  function canAdvance() {
    if (step === 'upload') return !!imageBase64;
    if (step === 'style') return !!selectedStyle;
    if (step === 'details') return !!(prefs.sqft && prefs.city && prefs.country);
    return false;
  }

  async function advance() {
    if (step === 'details') {
      setStep('results');
      setGenerating(true);
      setError('');
      setResults([]);
      try {
        await generateDesigns(
          imageBase64,
          imageMime,
          selectedStyle!.name,
          BUDGET_TIERS,
          prefs,
          (result) => setResults((prev) => [...prev, result]),
        );
      } catch (e) {
        setError(e instanceof Error ? e.message : 'Something went wrong. Please try again.');
      } finally {
        setGenerating(false);
      }
    } else {
      const next = STEPS[stepIndex + 1];
      if (next) setStep(next);
    }
  }

  function goBack() {
    if (step === 'results') {
      setStep('details');
      setResults([]);
    } else {
      const prev = STEPS[stepIndex - 1];
      if (prev) setStep(prev);
    }
  }

  return (
    <div className="min-h-screen" style={{ background: '#F5F5F0', color: '#141414' }}>
      {/* Header */}
      <header className="sticky top-0 z-10 backdrop-blur-sm border-b border-neutral-200/60" style={{ background: 'rgba(245,245,240,0.85)' }}>
        <div className="max-w-3xl mx-auto px-6 h-14 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Palette className="w-5 h-5 -rotate-12 text-neutral-700" />
            <span className="font-semibold text-lg tracking-tight">iDesign</span>
          </div>

          {/* Step indicator */}
          <div className="flex items-center gap-1.5">
            {STEPS.map((s, i) => (
              <div key={s} className="flex items-center gap-1.5">
                <div
                  className={`w-2 h-2 rounded-full transition-all duration-300
                    ${s === step ? 'bg-neutral-800 scale-125' : i < stepIndex ? 'bg-neutral-400' : 'bg-neutral-200'}`}
                />
                {i < STEPS.length - 1 && <div className="w-4 h-px bg-neutral-200" />}
              </div>
            ))}
            <span className="ml-3 text-xs text-neutral-400 font-medium">{STEP_LABELS[step]}</span>
          </div>
        </div>
      </header>

      {/* Room preview thumbnail (visible after upload) */}
      {imagePreview && step !== 'upload' && (
        <div className="max-w-3xl mx-auto px-6 pt-4 flex items-center gap-3">
          <img src={imagePreview} alt="Your room" className="w-12 h-12 rounded-lg object-cover border border-neutral-200" />
          {selectedStyle && (
            <span className="text-xs text-neutral-500 font-medium px-2.5 py-1 rounded-full bg-white border border-neutral-200">
              {selectedStyle.name}
            </span>
          )}
        </div>
      )}

      {/* Main content */}
      <main className="max-w-3xl mx-auto px-6 py-10">
        <AnimatePresence mode="wait">
          <motion.div
            key={step}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.28, ease: 'easeInOut' }}
          >
            {step === 'upload' && (
              <StepUpload
                onUpload={(base64, mime, preview) => {
                  setImageBase64(base64);
                  setImageMime(mime);
                  setImagePreview(preview);
                }}
              />
            )}
            {step === 'style' && (
              <StepStyle selected={selectedStyle} onSelect={setSelectedStyle} />
            )}
            {step === 'details' && (
              <StepDetails prefs={prefs} onChange={setPrefs} />
            )}
            {step === 'results' && (
              <>
                {error && (
                  <div className="mb-6 px-4 py-3 rounded-xl bg-red-50 border border-red-100 text-sm text-red-600">
                    {error}
                  </div>
                )}
                <StepResults results={results} tiers={BUDGET_TIERS} />
              </>
            )}
          </motion.div>
        </AnimatePresence>

        {/* Navigation */}
        {step !== 'results' && (
          <div className="flex items-center justify-between mt-10">
            {stepIndex > 0 ? (
              <button
                onClick={goBack}
                className="flex items-center gap-1.5 text-sm text-neutral-500 hover:text-neutral-700 transition-colors"
              >
                <ArrowLeft className="w-4 h-4" />
                Back
              </button>
            ) : (
              <div />
            )}
            <button
              onClick={advance}
              disabled={!canAdvance() || generating}
              className="flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold bg-neutral-800 text-white
                hover:bg-neutral-700 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
            >
              {step === 'details' ? 'Generate Designs' : 'Continue'}
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        )}

        {step === 'results' && !generating && (
          <div className="mt-10 flex justify-center">
            <button
              onClick={() => {
                setStep('upload');
                setImageBase64('');
                setImagePreview('');
                setSelectedStyle(null);
                setPrefs({ sqft: '', city: '', country: '' });
                setResults([]);
                setError('');
              }}
              className="text-sm text-neutral-400 hover:text-neutral-600 underline underline-offset-2 transition-colors"
            >
              Start over
            </button>
          </div>
        )}
      </main>
    </div>
  );
}
