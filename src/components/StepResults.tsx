import { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { ExternalLink, ShoppingBag, Loader2 } from 'lucide-react';
import type { DesignResult, BudgetTier } from '../types';

interface Props {
  results: DesignResult[];
  tiers: BudgetTier[];
}

export default function StepResults({ results, tiers }: Props) {
  const [activeId, setActiveId] = useState<string | null>(null);
  const isLoading = results.length < tiers.length;

  const activeResult = results.find((r) => r.tier.id === activeId);

  return (
    <div className="flex flex-col items-center gap-8 w-full">
      <div className="text-center space-y-3">
        <h2 className="text-3xl font-semibold tracking-tight" style={{ color: '#141414' }}>
          Your <span className="italic" style={{ fontFamily: 'Georgia, serif' }}>curated</span> proposals
        </h2>
        <p className="text-base text-neutral-500">
          {isLoading
            ? `Generating ${results.length} of ${tiers.length} proposals…`
            : 'Click any proposal to explore the shopping list.'}
        </p>
      </div>

      {/* 2×2 Grid */}
      <div className="grid grid-cols-2 gap-4 w-full max-w-2xl">
        {tiers.map((tier) => {
          const result = results.find((r) => r.tier.id === tier.id);
          const isActive = activeId === tier.id;

          return (
            <motion.div
              key={tier.id}
              whileHover={result ? { scale: 1.02 } : {}}
              onClick={() => result && setActiveId(isActive ? null : tier.id)}
              className={`relative rounded-2xl overflow-hidden border-2 transition-all
                ${result ? 'cursor-pointer' : 'cursor-default'}
                ${isActive ? 'border-neutral-800 shadow-xl' : 'border-transparent shadow-sm'}`}
            >
              {result ? (
                <>
                  <img src={result.imageUrl || '/placeholder.svg'} alt={tier.label} className="w-full h-44 object-cover" />
                  <div className="p-3 bg-white">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-neutral-800">{tier.label}</span>
                      <ShoppingBag className="w-4 h-4 text-neutral-400" />
                    </div>
                    <p className="text-xs text-neutral-400 mt-0.5 line-clamp-1">{tier.description}</p>
                  </div>
                </>
              ) : (
                <div className="w-full h-56 bg-neutral-100 flex flex-col items-center justify-center gap-3">
                  <Loader2 className="w-6 h-6 text-neutral-400 animate-spin" />
                  <span className="text-sm text-neutral-400 font-medium">{tier.label}</span>
                  <span className="text-xs text-neutral-300">Generating…</span>
                </div>
              )}
            </motion.div>
          );
        })}
      </div>

      {/* Shopping List Panel */}
      <AnimatePresence>
        {activeResult && (
          <motion.div
            key={activeResult.tier.id}
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 16 }}
            transition={{ duration: 0.25 }}
            className="w-full max-w-2xl rounded-2xl bg-white border border-neutral-200 shadow-md overflow-hidden"
          >
            <div className="px-6 py-4 border-b border-neutral-100 flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-neutral-800">{activeResult.tier.label} Shopping List</h3>
                <p className="text-xs text-neutral-400">{activeResult.tier.description}</p>
              </div>
              <span className="text-xs font-medium px-2.5 py-1 rounded-full bg-neutral-100 text-neutral-600">
                {activeResult.products.length} items
              </span>
            </div>
            <ul className="divide-y divide-neutral-50">
              {activeResult.products.map((product, i) => (
                <li key={i} className="flex items-center justify-between px-6 py-3 hover:bg-neutral-50 transition-colors">
                  <div className="flex-1 min-w-0 pr-4">
                    <p className="text-sm font-medium text-neutral-800 truncate">{product.name}</p>
                    <p className="text-xs text-neutral-400">{product.supplier}</p>
                  </div>
                  <div className="flex items-center gap-3 shrink-0">
                    <span className="text-sm font-semibold text-neutral-700">{product.price}</span>
                    <a
                      href={product.link}
                      target="_blank"
                      rel="noopener noreferrer"
                      onClick={(e) => e.stopPropagation()}
                      className="flex items-center gap-1 text-xs font-medium px-3 py-1.5 rounded-lg bg-neutral-800 text-white hover:bg-neutral-700 transition-colors"
                    >
                      Buy <ExternalLink className="w-3 h-3" />
                    </a>
                  </div>
                </li>
              ))}
            </ul>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
