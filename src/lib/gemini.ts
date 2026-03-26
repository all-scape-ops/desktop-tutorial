import { GoogleGenAI } from '@google/genai';
import type { BudgetTier, DesignResult, Product, UserPreferences } from '../types';

function getClient() {
  const key = import.meta.env.VITE_GEMINI_API_KEY as string;
  if (!key) throw new Error('VITE_GEMINI_API_KEY is not set.');
  return new GoogleGenAI({ apiKey: key });
}

const delay = (ms: number) => new Promise((r) => setTimeout(r, ms));

// One single API call returns products for ALL 4 tiers at once
async function sourceAllProducts(
  ai: GoogleGenAI,
  style: string,
  tiers: BudgetTier[],
  prefs: UserPreferences,
): Promise<Record<string, Product[]>> {
  const tierList = tiers
    .map((t) => `- $${t.amount} budget: ${t.description}`)
    .join('\n');

  const prompt = `You are an interior design product sourcer.
For each budget tier below, find real purchasable furniture and decor items matching the "${style}" style.
The room is in ${prefs.city}, ${prefs.country}.

Budget tiers:
${tierList}

Return ONLY a valid JSON object (no markdown) in this exact shape:
{
  "${tiers[0].id}": [{"name":"...","price":"$XX.XX","link":"https://www.amazon.com/...","supplier":"Amazon"}],
  "${tiers[1].id}": [...],
  "${tiers[2].id}": [...],
  "${tiers[3].id}": [...]
}

Rules for each tier:
- Max 5 items per tier.
- Sum of prices must be STRICTLY under the tier budget.
- Links must be real Amazon, Wayfair, IKEA, Target, or Home Depot product or search pages.
- Items must match the ${style} aesthetic.`;

  const response = await ai.models.generateContent({
    model: 'gemini-1.5-flash',
    contents: prompt,
  });

  const text = response.text ?? '{}';
  const jsonMatch = text.match(/\{[\s\S]*\}/);
  if (!jsonMatch) return {};
  try {
    return JSON.parse(jsonMatch[0]) as Record<string, Product[]>;
  } catch {
    return {};
  }
}

async function generateRoomImage(
  ai: GoogleGenAI,
  base64Image: string,
  mimeType: string,
  style: string,
  tier: BudgetTier,
  products: Product[],
  prefs: UserPreferences,
): Promise<string> {
  const productList = products.map((p) => `- ${p.name} (${p.price})`).join('\n');

  const structuralNote =
    tier.amount >= 2500
      ? 'You MAY change the flooring material and wall color or texture.'
      : tier.amount >= 1000
        ? 'Keep the existing floor and walls but update the furniture layout.'
        : 'Keep all structural elements (walls, floor, ceiling) unchanged.';

  const prompt = `You are an expert interior designer. Redesign this exact room in the "${style}" style by placing these products inside it:
${productList}

Rules:
- This MUST be the same room from the photo — same walls, same window positions, same dimensions.
- Place ALL listed products visibly inside the room.
- ${structuralNote}
- Room is approximately ${prefs.sqft} sq ft.
- Output a photorealistic interior photograph.`;

  const response = await ai.models.generateContent({
    model: 'gemini-2.0-flash-preview-image-generation',
    contents: [
      {
        role: 'user',
        parts: [
          { inlineData: { mimeType, data: base64Image } },
          { text: prompt },
        ],
      },
    ],
    config: { responseModalities: ['IMAGE', 'TEXT'] },
  });

  for (const part of response.candidates?.[0]?.content?.parts ?? []) {
    if (part.inlineData?.data) {
      return `data:${part.inlineData.mimeType};base64,${part.inlineData.data}`;
    }
  }
  return '';
}

export async function generateDesigns(
  base64Image: string,
  mimeType: string,
  style: string,
  tiers: BudgetTier[],
  prefs: UserPreferences,
  onTierComplete: (result: DesignResult) => void,
): Promise<void> {
  const ai = getClient();

  // Single call for all product lists
  const allProducts = await sourceAllProducts(ai, style, tiers, prefs);

  // Generate images one at a time with a 4-second gap to respect rate limits
  for (let i = 0; i < tiers.length; i++) {
    const tier = tiers[i];
    const products = allProducts[tier.id] ?? [];
    if (i > 0) await delay(4000);
    const imageUrl = await generateRoomImage(ai, base64Image, mimeType, style, tier, products, prefs);
    onTierComplete({ tier, products, imageUrl });
  }
}
