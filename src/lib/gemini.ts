import { GoogleGenAI } from '@google/genai';
import type { BudgetTier, DesignResult, Product, UserPreferences } from '../types';

function getClient() {
  const key = import.meta.env.VITE_GEMINI_API_KEY as string;
  if (!key) throw new Error('VITE_GEMINI_API_KEY is not set.');
  return new GoogleGenAI({ apiKey: key });
}

async function sourcePrducts(
  ai: GoogleGenAI,
  style: string,
  tier: BudgetTier,
  prefs: UserPreferences,
): Promise<Product[]> {
  const prompt = `You are an interior design product sourcer.
Find up to 6 real interior design items that match the "${style}" style with a TOTAL budget strictly under $${tier.amount}.
The items must be deliverable in ${prefs.city}, ${prefs.country}.
Room description: ${tier.description}

Return ONLY a valid JSON array (no markdown, no explanation) in this exact shape:
[{"name":"...","price":"$XX.XX","link":"https://...","supplier":"..."}]

Rules:
- Each link must be a direct product page (e.g. a specific Amazon or Wayfair product, not a search page).
- The sum of all prices must be strictly less than $${tier.amount}.
- Return no more than 6 items.`;

  const response = await ai.models.generateContent({
    model: 'gemini-2.0-flash',
    contents: prompt,
    config: {
      tools: [{ googleSearch: {} }],
    },
  });

  const text = response.text ?? '[]';
  const jsonMatch = text.match(/\[[\s\S]*\]/);
  if (!jsonMatch) return [];
  try {
    return JSON.parse(jsonMatch[0]) as Product[];
  } catch {
    return [];
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
  const productList = products
    .map((p) => `- ${p.name} (${p.price})`)
    .join('\n');

  const structuralNote =
    tier.amount >= 2500
      ? 'You MAY change the flooring material and wall color or texture.'
      : tier.amount >= 1000
        ? 'Keep the existing floor and walls but update the furniture layout.'
        : 'Keep all structural elements (walls, floor, ceiling) unchanged.';

  const prompt = `You are an expert interior designer. Redesign this room in the "${style}" style using EXACTLY the following products:
${productList}

Important rules:
- Include ALL listed products visibly in the redesigned room.
- Never leave the room empty or bare.
- ${structuralNote}
- The room is approximately ${prefs.sqft} sq ft.
- Produce a photorealistic, high-quality interior photograph.`;

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

  for (const tier of tiers) {
    const products = await sourcePrducts(ai, style, tier, prefs);
    const imageUrl = await generateRoomImage(ai, base64Image, mimeType, style, tier, products, prefs);
    onTierComplete({ tier, products, imageUrl });
  }
}
