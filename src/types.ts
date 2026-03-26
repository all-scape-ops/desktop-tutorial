export type RoomType = 'living' | 'kitchen' | 'bedroom';

export interface StyleOption {
  id: string;
  name: string;
  image: string;
  description: string;
}

export interface BudgetTier {
  id: string;
  label: string;
  amount: number;
  description: string;
}

export interface Product {
  name: string;
  price: string;
  link: string;
  supplier: string;
}

export interface DesignResult {
  imageUrl: string;
  tier: BudgetTier;
  products: Product[];
}

export interface UserPreferences {
  sqft: string;
  city: string;
  country: string;
}
