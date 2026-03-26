import type { StyleOption, BudgetTier } from '../types';

export const STYLE_OPTIONS: StyleOption[] = [
  {
    id: 'modern-minimalist',
    name: 'Modern Minimalist',
    image: 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=600&q=80',
    description: 'Clean lines, neutral palette, uncluttered spaces.',
  },
  {
    id: 'industrial-loft',
    name: 'Industrial Loft',
    image: 'https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=600&q=80',
    description: 'Raw materials, exposed brick, metal accents.',
  },
  {
    id: 'bohemian-chic',
    name: 'Bohemian Chic',
    image: 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=600&q=80',
    description: 'Warm tones, layered textures, global-inspired décor.',
  },
  {
    id: 'scandinavian',
    name: 'Scandinavian',
    image: 'https://images.unsplash.com/photo-1567225557594-88d73e55f2cb?w=600&q=80',
    description: 'Functional beauty, light woods, cosy hygge vibes.',
  },
];

export const BUDGET_TIERS: BudgetTier[] = [
  {
    id: 'tier-100',
    label: '$100',
    amount: 100,
    description: 'Decor & lighting refresh — pillows, wall art, smart bulbs.',
  },
  {
    id: 'tier-500',
    label: '$500',
    amount: 500,
    description: 'Decor + small furniture — rugs, side tables, lamps.',
  },
  {
    id: 'tier-1000',
    label: '$1,000',
    amount: 1000,
    description: 'Light remodel — new main furniture & statement lighting.',
  },
  {
    id: 'tier-2500',
    label: '$2,500',
    amount: 2500,
    description: 'Full remodel — flooring, wall treatments & premium sets.',
  },
];
