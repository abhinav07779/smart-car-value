// Currency conversion rates (in a real app, these would come from an API)
// INR is now the base currency (1.0)
export const currencyRates = {
  INR: 1.0,
  USD: 0.013,
  EUR: 0.011,
  GBP: 0.0097,
  JPY: 1.47,
  CAD: 0.017,
  AUD: 0.018,
  CHF: 0.012,
  CNY: 0.086,
  BRL: 0.069
};

export const currencySymbols = {
  INR: '₹',
  USD: '$',
  EUR: '€',
  GBP: '£',
  JPY: '¥',
  CAD: 'C$',
  AUD: 'A$',
  CHF: 'CHF',
  CNY: '¥',
  BRL: 'R$'
};

export const currencyNames = {
  INR: 'Indian Rupee',
  USD: 'US Dollar',
  EUR: 'Euro',
  GBP: 'British Pound',
  JPY: 'Japanese Yen',
  CAD: 'Canadian Dollar',
  AUD: 'Australian Dollar',
  CHF: 'Swiss Franc',
  CNY: 'Chinese Yuan',
  BRL: 'Brazilian Real'
};

export function convertPrice(inrPrice: number, targetCurrency: string): number {
  const rate = currencyRates[targetCurrency as keyof typeof currencyRates];
  return Math.round(inrPrice * rate);
}

export function formatCurrency(amount: number, currency: string): string {
  const symbol = currencySymbols[currency as keyof typeof currencySymbols];
  
  // Special formatting for currencies
  if (currency === 'JPY' || currency === 'CNY' || currency === 'INR') {
    return `${symbol}${Math.round(amount).toLocaleString()}`;
  }
  
  return `${symbol}${amount.toLocaleString()}`;
}

export function getAllCurrencyConversions(inrPrice: number) {
  return Object.keys(currencyRates).map(currency => ({
    currency,
    amount: convertPrice(inrPrice, currency),
    symbol: currencySymbols[currency as keyof typeof currencySymbols],
    name: currencyNames[currency as keyof typeof currencyNames],
    formatted: formatCurrency(convertPrice(inrPrice, currency), currency)
  }));
}