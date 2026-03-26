import type { DesignResult } from '../types';
import { BUDGET_TIERS } from './constants';

const DEMO_RESULTS: DesignResult[] = [
  {
    tier: BUDGET_TIERS[0],
    imageUrl: 'https://images.unsplash.com/photo-1616594039964-ae9021a400a0?w=800&q=80',
    products: [
      {
        name: 'Linen Throw Pillow Set (4pc)',
        price: '$24.99',
        link: 'https://www.amazon.com/s?k=linen+throw+pillow+set',
        supplier: 'Amazon',
      },
      {
        name: 'Woven Macramé Wall Art 24"',
        price: '$19.99',
        link: 'https://www.amazon.com/s?k=macrame+wall+art',
        supplier: 'Amazon',
      },
      {
        name: 'Philips Hue White Smart Bulb 2-Pack',
        price: '$24.99',
        link: 'https://www.target.com/s?searchTerm=philips+hue+smart+bulb',
        supplier: 'Target',
      },
      {
        name: 'Minimalist Ceramic Vase',
        price: '$12.99',
        link: 'https://www.target.com/s?searchTerm=minimalist+ceramic+vase',
        supplier: 'Target',
      },
    ],
  },
  {
    tier: BUDGET_TIERS[1],
    imageUrl: 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800&q=80',
    products: [
      {
        name: 'Jute Area Rug 5×8 ft',
        price: '$89.00',
        link: 'https://www.wayfair.com/keyword.php?keyword=jute+area+rug+5x8',
        supplier: 'Wayfair',
      },
      {
        name: 'Mid-Century Round Side Table',
        price: '$119.00',
        link: 'https://www.wayfair.com/keyword.php?keyword=mid+century+side+table',
        supplier: 'Wayfair',
      },
      {
        name: 'IKEA HEKTAR Floor Lamp',
        price: '$69.99',
        link: 'https://www.ikea.com/us/en/search/?q=floor+lamp',
        supplier: 'IKEA',
      },
      {
        name: 'Velvet Accent Pillow (2pc)',
        price: '$34.99',
        link: 'https://www.target.com/s?searchTerm=velvet+accent+pillow',
        supplier: 'Target',
      },
      {
        name: 'Gallery Wall Frame Set (6pc)',
        price: '$49.99',
        link: 'https://www.amazon.com/s?k=gallery+wall+frame+set',
        supplier: 'Amazon',
      },
    ],
  },
  {
    tier: BUDGET_TIERS[2],
    imageUrl: 'https://images.unsplash.com/photo-1567225557594-88d73e55f2cb?w=800&q=80',
    products: [
      {
        name: 'IKEA SÖDERHAMN 3-Seat Sofa',
        price: '$649.00',
        link: 'https://www.ikea.com/us/en/search/?q=sofa+3+seat',
        supplier: 'IKEA',
      },
      {
        name: 'Rattan Woven Pendant Light',
        price: '$89.99',
        link: 'https://www.amazon.com/s?k=rattan+pendant+light',
        supplier: 'Amazon',
      },
      {
        name: 'Solid Acacia Wood Coffee Table',
        price: '$189.00',
        link: 'https://www.wayfair.com/keyword.php?keyword=solid+wood+coffee+table',
        supplier: 'Wayfair',
      },
      {
        name: 'Large Abstract Canvas Print',
        price: '$49.99',
        link: 'https://www.amazon.com/s?k=large+abstract+canvas+wall+art',
        supplier: 'Amazon',
      },
    ],
  },
  {
    tier: BUDGET_TIERS[3],
    imageUrl: 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800&q=80',
    products: [
      {
        name: 'LifeProof Vinyl Plank Flooring (200 sqft)',
        price: '$398.00',
        link: 'https://www.homedepot.com/s/vinyl%20plank%20flooring',
        supplier: 'Home Depot',
      },
      {
        name: 'Behr Premium Feature Wall Paint (2 gal)',
        price: '$98.00',
        link: 'https://www.homedepot.com/s/behr+premium+interior+paint',
        supplier: 'Home Depot',
      },
      {
        name: 'West Elm Harmony Sectional Sofa',
        price: '$1,299.00',
        link: 'https://www.westelm.com/search/results.html?words=sectional+sofa',
        supplier: 'West Elm',
      },
      {
        name: 'Rejuvenation Pendant Light Set (2pc)',
        price: '$398.00',
        link: 'https://www.amazon.com/s?k=modern+pendant+light+set',
        supplier: 'Amazon',
      },
    ],
  },
];

export async function generateDesignsDemo(
  onTierComplete: (result: DesignResult) => void,
): Promise<void> {
  for (const result of DEMO_RESULTS) {
    await new Promise((r) => setTimeout(r, 1200));
    onTierComplete(result);
  }
}
