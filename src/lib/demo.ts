import type { DesignResult } from '../types';
import { BUDGET_TIERS } from './constants';

const DEMO_RESULTS: DesignResult[] = [
  {
    tier: BUDGET_TIERS[0],
    imageUrl: 'https://images.unsplash.com/photo-1616594039964-ae9021a400a0?w=800&q=80',
    products: [
      { name: 'Linen Throw Pillow Set (4pc)', price: '$24.99', link: '#', supplier: 'Amazon' },
      { name: 'Woven Macramé Wall Art', price: '$18.00', link: '#', supplier: 'Etsy' },
      { name: 'Philips Hue Smart Bulb (2pk)', price: '$29.99', link: '#', supplier: 'Best Buy' },
      { name: 'Minimalist Ceramic Vase', price: '$14.99', link: '#', supplier: 'Target' },
    ],
  },
  {
    tier: BUDGET_TIERS[1],
    imageUrl: 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800&q=80',
    products: [
      { name: 'Jute Area Rug 5×8 ft', price: '$89.00', link: '#', supplier: 'Wayfair' },
      { name: 'Mid-Century Side Table', price: '$129.00', link: '#', supplier: 'West Elm' },
      { name: 'Arc Floor Lamp', price: '$119.99', link: '#', supplier: 'IKEA' },
      { name: 'Velvet Accent Pillow', price: '$34.99', link: '#', supplier: 'H&M Home' },
      { name: 'Gallery Wall Frame Set', price: '$49.99', link: '#', supplier: 'Target' },
    ],
  },
  {
    tier: BUDGET_TIERS[2],
    imageUrl: 'https://images.unsplash.com/photo-1567225557594-88d73e55f2cb?w=800&q=80',
    products: [
      { name: '3-Seat Linen Sofa', price: '$649.00', link: '#', supplier: 'Article' },
      { name: 'Rattan Pendant Light', price: '$129.99', link: '#', supplier: 'Anthropologie' },
      { name: 'Solid Wood Coffee Table', price: '$189.00', link: '#', supplier: 'CB2' },
      { name: 'Abstract Canvas Print', price: '$79.00', link: '#', supplier: 'Minted' },
    ],
  },
  {
    tier: BUDGET_TIERS[3],
    imageUrl: 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800&q=80',
    products: [
      { name: 'Premium Hardwood Flooring (200 sqft)', price: '$799.00', link: '#', supplier: 'Home Depot' },
      { name: 'Sherwin-Williams Feature Wall Paint', price: '$89.00', link: '#', supplier: 'Sherwin-Williams' },
      { name: 'Modular Sectional Sofa', price: '$1,199.00', link: '#', supplier: 'Pottery Barn' },
      { name: 'Designer Pendant Lighting Set', price: '$349.00', link: '#', supplier: 'Lumens' },
    ],
  },
];

export async function generateDesignsDemo(
  onTierComplete: (result: DesignResult) => void,
): Promise<void> {
  for (const result of DEMO_RESULTS) {
    await new Promise((r) => setTimeout(r, 1200)); // simulate loading
    onTierComplete(result);
  }
}
