import { motion } from 'motion/react';
import { Check } from 'lucide-react';
import { STYLE_OPTIONS } from '../lib/constants';
import type { StyleOption } from '../types';

interface Props {
  selected: StyleOption | null;
  onSelect: (style: StyleOption) => void;
}

export default function StepStyle({ selected, onSelect }: Props) {
  return (
    <div className="flex flex-col items-center gap-8">
      <div className="text-center space-y-3">
        <h2 className="text-3xl font-semibold tracking-tight" style={{ color: '#141414' }}>
          Choose your aesthetic
        </h2>
        <p className="text-base text-neutral-500 max-w-md">
          Select the design style that resonates with your vision.
        </p>
      </div>

      <div className="grid grid-cols-2 gap-4 w-full max-w-2xl">
        {STYLE_OPTIONS.map((style) => {
          const isSelected = selected?.id === style.id;
          return (
            <motion.div
              key={style.id}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => onSelect(style)}
              className={`relative rounded-2xl overflow-hidden cursor-pointer border-2 transition-all
                ${isSelected ? 'border-neutral-800 shadow-lg' : 'border-transparent shadow-sm hover:shadow-md'}`}
            >
              <img
                src={style.image}
                alt={style.name}
                className="w-full h-40 object-cover"
              />
              <div className="p-3 bg-white">
                <p className="font-semibold text-sm text-neutral-800">{style.name}</p>
                <p className="text-xs text-neutral-400 mt-0.5">{style.description}</p>
              </div>
              {isSelected && (
                <div className="absolute top-2 right-2 w-7 h-7 rounded-full bg-neutral-800 flex items-center justify-center">
                  <Check className="w-4 h-4 text-white" />
                </div>
              )}
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
