import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { Car, Calculator, TrendingUp, Globe, ExternalLink, Star, Shield, Zap } from "lucide-react";
import { getAllCurrencyConversions, formatCurrency, convertPrice } from "@/utils/currency";

interface CarData {
  brand: string;
  model: string;
  year: number;
  kmDriven: number;
  fuelType: string;
  transmission: string;
  engineSize: number;
  city: string;
  state: string;
  cngKit: boolean;
  qualityScore: number;
}

interface PredictionResult {
  predictedPrice: number;
  confidence: number;
  rmse: number;
  r2Score: number;
}

// Comprehensive car models data for each brand
const carModelsData: { [key: string]: string[] } = {
  "Maruti Suzuki": [
    "Alto", "Alto K10", "S-Presso", "Celerio", "Wagon R", "Swift", "Swift Dzire", 
    "Baleno", "Baleno RS", "Ignis", "Ciaz", "Ertiga", "XL6", "Vitara Brezza", 
    "S-Cross", "Grand Vitara", "Jimny", "Fronx", "Invicto"
  ],
  "Hyundai": [
    "Santro", "Grand i10", "Grand i10 Nios", "i20", "i20 N Line", "Verna", 
    "Elantra", "Creta", "Venue", "Tucson", "Kona Electric", "Ioniq 5", 
    "Alcazar", "Aura", "Xcent"
  ],
  "Tata": [
    "Nano", "Tiago", "Tigor", "Altroz", "Punch", "Nexon", "Nexon EV", 
    "Harrier", "Safari", "Hexa", "Zest", "Bolt", "Indica", "Indigo", "Sumo"
  ],
  "Mahindra": [
    "KUV100", "XUV300", "XUV400", "XUV700", "Scorpio", "Scorpio N", 
    "Bolero", "Bolero Neo", "Thar", "Marazzo", "Xylo", "TUV300", "KUV100 NXT"
  ],
  "Toyota": [
    "Glanza", "Urban Cruiser", "Innova Crysta", "Innova HyCross", "Fortuner", 
    "Camry", "Vellfire", "Land Cruiser", "Prius", "Corolla Altis", "Etios", 
    "Etios Liva", "Qualis"
  ],
  "Honda": [
    "Amaze", "City", "Civic", "Accord", "CR-V", "WR-V", "Jazz", "Brio", 
    "Mobilio", "BR-V", "Ridgeline"
  ],
  "Ford": [
    "EcoSport", "Endeavour", "Figo", "Aspire", "Freestyle", "Mustang", 
    "Fiesta", "Ikon", "Fusion", "Territory"
  ],
  "Volkswagen": [
    "Polo", "Vento", "Virtus", "Taigun", "Tiguan", "Passat", "Jetta", 
    "Beetle", "T-Roc", "ID.4"
  ],
  "Skoda": [
    "Rapid", "Slavia", "Kushaq", "Kodiaq", "Superb", "Octavia", "Fabia", 
    "Laura", "Yeti", "Kamiq"
  ],
  "Nissan": [
    "Micra", "Sunny", "Terrano", "Kicks", "Magnite", "GT-R", "370Z", 
    "Pathfinder", "X-Trail", "Navara"
  ],
  "Renault": [
    "Kwid", "Triber", "Duster", "Captur", "Lodgy", "Scala", "Pulse", 
    "Fluence", "Koleos", "Kiger"
  ],
  "Kia": [
    "Seltos", "Sonet", "Carens", "Carnival", "EV6", "Stonic", "Rio", 
    "Optima", "Sportage", "Sorento"
  ],
  "BMW": [
    "1 Series", "2 Series", "3 Series", "4 Series", "5 Series", "6 Series", 
    "7 Series", "8 Series", "X1", "X2", "X3", "X4", "X5", "X6", "X7", 
    "Z4", "i3", "i4", "iX", "iX3", "i8"
  ],
  "Mercedes": [
    "A-Class", "B-Class", "C-Class", "E-Class", "S-Class", "CLA", "CLS", 
    "GLA", "GLB", "GLC", "GLE", "GLS", "G-Class", "AMG GT", "EQC", "EQS", 
    "EQA", "EQB", "EQE", "EQS SUV"
  ],
  "Audi": [
    "A1", "A3", "A4", "A5", "A6", "A7", "A8", "Q2", "Q3", "Q4 e-tron", 
    "Q5", "Q7", "Q8", "TT", "R8", "e-tron", "e-tron GT", "RS3", "RS4", 
    "RS5", "RS6", "RS7", "RS Q8"
  ]
};

// Top 5 cities for each state in India
const stateCitiesData: { [key: string]: string[] } = {
  "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad"],
  "Delhi": ["New Delhi", "Central Delhi", "East Delhi", "North Delhi", "South Delhi"],
  "Karnataka": ["Bangalore", "Mysore", "Hubli", "Mangalore", "Belgaum"],
  "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem"],
  "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Khammam", "Karimnagar"],
  "West Bengal": ["Kolkata", "Howrah", "Durgapur", "Asansol", "Siliguri"],
  "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar"],
  "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Kota", "Ajmer"],
  "Uttar Pradesh": ["Lucknow", "Kanpur", "Agra", "Varanasi", "Meerut"],
  "Punjab": ["Chandigarh", "Ludhiana", "Amritsar", "Jalandhar", "Patiala"],
  "Haryana": ["Gurgaon", "Faridabad", "Panipat", "Karnal", "Hisar"],
  "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur", "Kollam"],
  "Madhya Pradesh": ["Bhopal", "Indore", "Gwalior", "Jabalpur", "Ujjain"],
  "Bihar": ["Patna", "Gaya", "Bhagalpur", "Muzaffarpur", "Darbhanga"],
  "Odisha": ["Bhubaneswar", "Cuttack", "Rourkela", "Berhampur", "Sambalpur"]
};

// Helper function to format brand and model names for CarDekho URLs
const formatCarDekhoUrl = (brand: string, model: string): string => {
  // Brand mapping for CarDekho specific naming conventions
  const brandMapping: { [key: string]: string } = {
    "Maruti Suzuki": "maruti-suzuki",
    "Hyundai": "hyundai",
    "Tata": "tata",
    "Mahindra": "mahindra",
    "Toyota": "toyota",
    "Honda": "honda",
    "Ford": "ford",
    "Volkswagen": "volkswagen",
    "Skoda": "skoda",
    "Nissan": "nissan",
    "Renault": "renault",
    "Kia": "kia",
    "BMW": "bmw",
    "Mercedes": "mercedes-benz",
    "Audi": "audi"
  };

  // Model mapping for specific CarDekho model names
  const modelMapping: { [key: string]: string } = {
    "Swift Dzire": "swift-dzire",
    "Grand i10": "grand-i10",
    "Grand i10 Nios": "grand-i10-nios",
    "i20 N Line": "i20-n-line",
    "XUV300": "xuv300",
    "XUV400": "xuv400",
    "XUV700": "xuv700",
    "Scorpio N": "scorpio-n",
    "Bolero Neo": "bolero-neo",
    "Innova Crysta": "innova-crysta",
    "Innova HyCross": "innova-hycross",
    "Land Cruiser": "land-cruiser",
    "Corolla Altis": "corolla-altis",
    "Etios Liva": "etios-liva",
    "WR-V": "wr-v",
    "BR-V": "br-v",
    "EcoSport": "ecosport",
    "Endeavour": "endeavour",
    "Freestyle": "freestyle",
    "Territory": "territory",
    "Virtus": "virtus",
    "Taigun": "taigun",
    "Tiguan": "tiguan",
    "T-Roc": "t-roc",
    "ID.4": "id4",
    "Slavia": "slavia",
    "Kushaq": "kushaq",
    "Kodiaq": "kodiaq",
    "Superb": "superb",
    "Octavia": "octavia",
    "Fabia": "fabia",
    "Laura": "laura",
    "Yeti": "yeti",
    "Kamiq": "kamiq",
    "Terrano": "terrano",
    "Kicks": "kicks",
    "Magnite": "magnite",
    "GT-R": "gt-r",
    "370Z": "370z",
    "Pathfinder": "pathfinder",
    "X-Trail": "x-trail",
    "Navara": "navara",
    "Triber": "triber",
    "Duster": "duster",
    "Captur": "captur",
    "Lodgy": "lodgy",
    "Scala": "scala",
    "Pulse": "pulse",
    "Fluence": "fluence",
    "Koleos": "koleos",
    "Kiger": "kiger",
    "Seltos": "seltos",
    "Sonet": "sonet",
    "Carens": "carens",
    "Carnival": "carnival",
    "EV6": "ev6",
    "Stonic": "stonic",
    "Rio": "rio",
    "Optima": "optima",
    "Sportage": "sportage",
    "Sorento": "sorento",
    "1 Series": "1-series",
    "2 Series": "2-series",
    "3 Series": "3-series",
    "4 Series": "4-series",
    "5 Series": "5-series",
    "6 Series": "6-series",
    "7 Series": "7-series",
    "8 Series": "8-series",
    "A-Class": "a-class",
    "B-Class": "b-class",
    "C-Class": "c-class",
    "E-Class": "e-class",
    "S-Class": "s-class",
    "CLA": "cla",
    "CLS": "cls",
    "GLA": "gla",
    "GLB": "glb",
    "GLC": "glc",
    "GLE": "gle",
    "GLS": "gls",
    "G-Class": "g-class",
    "AMG GT": "amg-gt",
    "EQC": "eqc",
    "EQS": "eqs",
    "EQA": "eqa",
    "EQB": "eqb",
    "EQE": "eqe",
    "EQS SUV": "eqs-suv",
    "Q2": "q2",
    "Q3": "q3",
    "Q4 e-tron": "q4-etron",
    "Q5": "q5",
    "Q7": "q7",
    "Q8": "q8",
    "TT": "tt",
    "R8": "r8",
    "e-tron": "etron",
    "e-tron GT": "etron-gt",
    "RS3": "rs3",
    "RS4": "rs4",
    "RS5": "rs5",
    "RS6": "rs6",
    "RS7": "rs7",
    "RS Q8": "rs-q8"
  };

  const formattedBrand = brandMapping[brand] || brand.toLowerCase().replace(/\s+/g, '-');
  const formattedModel = modelMapping[model] || model.toLowerCase().replace(/\s+/g, '-');
  
  // Generate multiple URL patterns for better coverage
  const urlPatterns = [
    // Most specific: Direct car model page
    `https://www.cardekho.com/carmodels/${formattedBrand}/${formattedModel}`,
    // Used cars with brand/model filter
    `https://www.cardekho.com/used-cars/${formattedBrand}/${formattedModel}`,
    // Search with brand and model parameters
    `https://www.cardekho.com/used-cars?brand=${encodeURIComponent(brand)}&model=${encodeURIComponent(model)}`,
    // General search fallback
    `https://www.cardekho.com/used-cars?q=${encodeURIComponent(brand)}+${encodeURIComponent(model)}`
  ];
  
  // Return the most specific URL (carmodels) as primary
  // This will take users directly to the specific car model page
  const finalUrl = urlPatterns[0];
  
  // Log the generated URL for debugging (remove in production)
  console.log(`CarDekho URL generated for ${brand} ${model}:`, finalUrl);
  
  return finalUrl;
};

// Top 3 car price comparison resources for Indian market (OLX as main preference)
const carPriceResources = [
  {
    name: "OLX Autos",
    url: "https://www.olx.in",
    description: "India's most popular classified platform with extensive car listings",
    rating: 4.6,
    features: ["Direct seller contact", "Price negotiation", "Local listings"],
    icon: "📱",
    searchUrl: (brand: string, model: string) => `https://www.olx.in/cars_c84?q=${encodeURIComponent(brand)}+${encodeURIComponent(model)}`,
    isMain: true
  },
  {
    name: "CarDekho",
    url: "https://www.cardekho.com",
    description: "Direct links to specific car model pages with detailed specs",
    rating: 4.8,
    features: ["Model-specific pages", "Detailed specifications", "Price comparison"],
    icon: "🚗",
    searchUrl: formatCarDekhoUrl
  },
  {
    name: "Cars24",
    url: "https://www.cars24.com",
    description: "Instant buying platform with inspections and warranties",
    rating: 4.5,
    features: ["Inspected cars", "Quick purchase", "Warranty options"],
    icon: "⚡",
    searchUrl: (brand: string, model: string) => `https://www.cars24.com/buy-used-cars/${brand.toLowerCase().replace(/\s+/g, '-')}/${model.toLowerCase().replace(/\s+/g, '-')}`
  }
];

export const CarPricePredictor = () => {
  const [carData, setCarData] = useState<CarData>({
    brand: "",
    model: "",
    year: 2020,
    kmDriven: 50000,
    fuelType: "",
    transmission: "",
    engineSize: 2.0,
    city: "",
    state: "",
    cngKit: false,
    qualityScore: 8.0
  });

  const [prediction, setPrediction] = useState<PredictionResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [availableModels, setAvailableModels] = useState<string[]>([]);
  const [selectedCurrency, setSelectedCurrency] = useState('INR');
  const [availableCities, setAvailableCities] = useState<string[]>([]);
  const [usedBackend, setUsedBackend] = useState<boolean | null>(null);
  const [apiUrlUsed, setApiUrlUsed] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // Update available models when brand changes
  useEffect(() => {
    if (carData.brand && carModelsData[carData.brand]) {
      setAvailableModels(carModelsData[carData.brand]);
      // Reset model when brand changes
      setCarData(prev => ({ ...prev, model: "" }));
    } else {
      setAvailableModels([]);
    }
  }, [carData.brand]);

  // Update available cities when state changes
  useEffect(() => {
    if (carData.state && stateCitiesData[carData.state]) {
      setAvailableCities(stateCitiesData[carData.state]);
      // Reset city when state changes
      setCarData(prev => ({ ...prev, city: "" }));
    } else {
      setAvailableCities([]);
    }
  }, [carData.state]);

  // Real ML API prediction
  const predictPrice = async () => {
    setIsLoading(true);
    setErrorMessage(null);
    
    try {
      const apiUrl = "https://smart-car-value.onrender.com";
      setApiUrlUsed(apiUrl);
      const response = await fetch(`${apiUrl}/predict`, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json" 
        },
        body: JSON.stringify(carData)
      });

      if (!response.ok) {
        const text = await response.text().catch(() => "");
        throw new Error(`API ${response.status} ${text ? `- ${text}` : ''}`.trim());
      }

      const result = await response.json();
      
      setPrediction({
        predictedPrice: result.predictedPrice,
        confidence: result.confidence,
        rmse: result.rmse,
        r2Score: result.r2Score
      });
      setUsedBackend(true);
      
    } catch (error) {
      console.error("Prediction error:", error);
      setUsedBackend(false);
      setErrorMessage(error instanceof Error ? error.message : "Prediction failed");
      setPrediction(null);
    }
    
    setIsLoading(false);
  };

  const getBrandMultiplier = (brand: string): number => {
    // Indian car market brand values
    const brandValues: { [key: string]: number } = {
      "Mercedes": 3.5, "BMW": 3.2, "Audi": 3.0, "Lexus": 2.8,
      "Toyota": 1.4, "Honda": 1.35, "Hyundai": 1.2, "Maruti Suzuki": 1.0,
      "Tata": 0.9, "Mahindra": 0.95, "Ford": 1.1, "Volkswagen": 1.25,
      "Nissan": 1.15, "Kia": 1.1, "Skoda": 1.2, "Renault": 0.85
    };
    return brandValues[brand] || 1.0;
  };

  const getFuelTypeFactor = (fuelType: string): number => {
    const fuelValues: { [key: string]: number } = {
      "Petrol": 1.0, "Diesel": 1.15, "CNG": 0.9, "LPG": 0.85,
      "Electric": 1.3, "Hybrid": 1.2
    };
    return fuelValues[fuelType] || 1.0;
  };

  const getLocationFactor = (city: string, state: string): number => {
    // Metropolitan cities have higher prices
    const metroMultiplier: { [key: string]: number } = {
      "Mumbai": 1.25, "Delhi": 1.2, "Bangalore": 1.15, "Chennai": 1.1,
      "Hyderabad": 1.1, "Pune": 1.15, "Kolkata": 1.05, "Ahmedabad": 1.05
    };
    
    const stateMultiplier: { [key: string]: number } = {
      "Maharashtra": 1.1, "Karnataka": 1.05, "Tamil Nadu": 1.0,
      "Delhi": 1.15, "Gujarat": 1.05, "West Bengal": 0.95,
      "Rajasthan": 0.9, "Uttar Pradesh": 0.85
    };
    
    return (metroMultiplier[city] || 1.0) * (stateMultiplier[state] || 0.95);
  };

  return (
    <div className="w-full max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center space-y-4">
        <div className="flex items-center justify-center gap-3">
          <Car className="h-8 w-8 text-primary" />
          <h1 className="text-4xl font-bold bg-gradient-hero bg-clip-text text-transparent">
            Car Price Predictor
          </h1>
        </div>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Real Random Forest ML Model with 91.96% accuracy trained on Indian car market data
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Input Form */}
        <Card className="shadow-card">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Calculator className="h-5 w-5" />
              Car Details
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="brand">Brand</Label>
                <Select value={carData.brand} onValueChange={(value) => setCarData({...carData, brand: value})}>
                  <SelectTrigger id="brand">
                    <SelectValue placeholder="Select brand" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Maruti Suzuki">Maruti Suzuki</SelectItem>
                    <SelectItem value="Hyundai">Hyundai</SelectItem>
                    <SelectItem value="Tata">Tata</SelectItem>
                    <SelectItem value="Mahindra">Mahindra</SelectItem>
                    <SelectItem value="Toyota">Toyota</SelectItem>
                    <SelectItem value="Honda">Honda</SelectItem>
                    <SelectItem value="Ford">Ford</SelectItem>
                    <SelectItem value="Volkswagen">Volkswagen</SelectItem>
                    <SelectItem value="Skoda">Skoda</SelectItem>
                    <SelectItem value="Nissan">Nissan</SelectItem>
                    <SelectItem value="Renault">Renault</SelectItem>
                    <SelectItem value="Kia">Kia</SelectItem>
                    <SelectItem value="BMW">BMW</SelectItem>
                    <SelectItem value="Mercedes">Mercedes</SelectItem>
                    <SelectItem value="Audi">Audi</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="model">Model</Label>
                <Select 
                  value={carData.model} 
                  onValueChange={(value) => setCarData({...carData, model: value})}
                  disabled={!carData.brand || availableModels.length === 0}
                >
                  <SelectTrigger id="model">
                    <SelectValue placeholder={!carData.brand ? "Select brand first" : "Select model"} />
                  </SelectTrigger>
                  <SelectContent>
                    {availableModels.map((model) => (
                      <SelectItem key={model} value={model}>
                        {model}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="year">Year</Label>
                <Input
                  id="year"
                  type="number"
                  value={carData.year}
                  onChange={(e) => setCarData({...carData, year: parseInt(e.target.value)})}
                  min="1990"
                  max="2024"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="kmDriven">Kilometers Driven</Label>
                <Input
                  id="kmDriven"
                  type="number"
                  value={carData.kmDriven}
                  onChange={(e) => setCarData({...carData, kmDriven: parseInt(e.target.value)})}
                  min="0"
                  placeholder="e.g., 45000"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="fuelType">Fuel Type</Label>
                <Select value={carData.fuelType} onValueChange={(value) => setCarData({...carData, fuelType: value})}>
                  <SelectTrigger id="fuelType">
                    <SelectValue placeholder="Select fuel type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Petrol">Petrol</SelectItem>
                    <SelectItem value="Diesel">Diesel</SelectItem>
                    <SelectItem value="CNG">CNG</SelectItem>
                    <SelectItem value="LPG">LPG</SelectItem>
                    <SelectItem value="Electric">Electric</SelectItem>
                    <SelectItem value="Hybrid">Hybrid</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="transmission">Transmission</Label>
                <Select value={carData.transmission} onValueChange={(value) => setCarData({...carData, transmission: value})}>
                  <SelectTrigger id="transmission">
                    <SelectValue placeholder="Select transmission" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Manual">Manual</SelectItem>
                    <SelectItem value="Automatic">Automatic</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="state">State</Label>
                <Select value={carData.state} onValueChange={(value) => setCarData({...carData, state: value})}>
                  <SelectTrigger id="state">
                    <SelectValue placeholder="Select state" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Maharashtra">Maharashtra</SelectItem>
                    <SelectItem value="Delhi">Delhi</SelectItem>
                    <SelectItem value="Karnataka">Karnataka</SelectItem>
                    <SelectItem value="Tamil Nadu">Tamil Nadu</SelectItem>
                    <SelectItem value="Telangana">Telangana</SelectItem>
                    <SelectItem value="West Bengal">West Bengal</SelectItem>
                    <SelectItem value="Gujarat">Gujarat</SelectItem>
                    <SelectItem value="Rajasthan">Rajasthan</SelectItem>
                    <SelectItem value="Uttar Pradesh">Uttar Pradesh</SelectItem>
                    <SelectItem value="Punjab">Punjab</SelectItem>
                    <SelectItem value="Haryana">Haryana</SelectItem>
                    <SelectItem value="Kerala">Kerala</SelectItem>
                    <SelectItem value="Madhya Pradesh">Madhya Pradesh</SelectItem>
                    <SelectItem value="Bihar">Bihar</SelectItem>
                    <SelectItem value="Odisha">Odisha</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="city">City</Label>
                <Select 
                  value={carData.city} 
                  onValueChange={(value) => setCarData({...carData, city: value})}
                  disabled={!carData.state || availableCities.length === 0}
                >
                  <SelectTrigger id="city">
                    <SelectValue placeholder={!carData.state ? "Select state first" : "Select city"} />
                  </SelectTrigger>
                  <SelectContent>
                    {availableCities.map((city) => (
                      <SelectItem key={city} value={city}>
                        {city}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="engineSize">Engine Size (L)</Label>
                <Input
                  id="engineSize"
                  type="number"
                  step="0.1"
                  value={carData.engineSize}
                  onChange={(e) => setCarData({...carData, engineSize: parseFloat(e.target.value)})}
                  min="0.5"
                  max="8.0"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="qualityScore">Quality Score (1-10)</Label>
                <Input
                  id="qualityScore"
                  type="number"
                  step="0.1"
                  value={carData.qualityScore}
                  onChange={(e) => setCarData({...carData, qualityScore: parseFloat(e.target.value)})}
                  min="1"
                  max="10"
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="cngKit" className="flex items-center gap-2">
                <input
                  type="checkbox"
                  id="cngKit"
                  checked={carData.cngKit}
                  onChange={(e) => setCarData({...carData, cngKit: e.target.checked})}
                  className="rounded"
                />
                CNG Kit Installed
              </Label>
            </div>

              <div className="space-y-2">
              <Label htmlFor="currency">Display Currency</Label>
              <Select value={selectedCurrency} onValueChange={setSelectedCurrency}>
                <SelectTrigger id="currency">
                  <SelectValue placeholder="Select currency" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="INR">INR (₹) - Indian Rupee</SelectItem>
                  <SelectItem value="USD">USD ($) - US Dollar</SelectItem>
                  <SelectItem value="EUR">EUR (€) - Euro</SelectItem>
                  <SelectItem value="GBP">GBP (£) - British Pound</SelectItem>
                  <SelectItem value="JPY">JPY (¥) - Japanese Yen</SelectItem>
                  <SelectItem value="CAD">CAD (C$) - Canadian Dollar</SelectItem>
                  <SelectItem value="AUD">AUD (A$) - Australian Dollar</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <Button 
              onClick={predictPrice}
              disabled={isLoading || !carData.brand || !carData.model || !carData.fuelType || !carData.transmission || !carData.city || !carData.state}
              className="w-full bg-gradient-hero hover:opacity-90 shadow-glow"
              size="lg"
            >
              {isLoading ? "Predicting with ML Model..." : "Predict Price with Real ML"}
            </Button>
          </CardContent>
        </Card>

        {/* Prediction Results */}
        <Card className="shadow-card">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5" />
              Prediction Results
            </CardTitle>
          </CardHeader>
          <CardContent>
            {prediction ? (
              <div className="space-y-6">
                {/* Primary Price in Selected Currency */}
                <div className="text-center p-6 bg-gradient-card rounded-lg">
                  <div className="text-3xl font-bold text-primary mb-2">
                    {formatCurrency(convertPrice(prediction.predictedPrice, selectedCurrency), selectedCurrency)}
                  </div>
                  <div className="flex items-center justify-center gap-2">
                    <Badge variant="secondary" className="text-sm">
                      {prediction.confidence}% Confidence
                    </Badge>
                    {usedBackend !== null && (
                      <Badge variant={usedBackend ? "default" : "destructive"} className="text-xs">
                        {usedBackend ? "Source: ML API" : "Source: Fallback"}
                      </Badge>
                    )}
                  </div>
                </div>

                {/* Multi-Currency Display */}
                <div className="space-y-4">
                  <div className="flex items-center gap-2 text-sm font-medium">
                    <Globe className="h-4 w-4" />
                    Price in Multiple Currencies
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    {getAllCurrencyConversions(prediction.predictedPrice)
                      .filter(conv => conv.currency !== selectedCurrency)
                      .slice(0, 6)
                      .map((conversion) => (
                      <div key={conversion.currency} className="flex justify-between items-center p-3 border rounded-lg bg-muted/50">
                        <div>
                          <div className="text-sm font-medium">{conversion.currency}</div>
                          <div className="text-xs text-muted-foreground">{conversion.name}</div>
                        </div>
                        <div className="text-right">
                          <div className="font-semibold">{conversion.formatted}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center p-4 border rounded-lg">
                    <div className="text-2xl font-semibold text-accent">
                      {formatCurrency(convertPrice(prediction.rmse, selectedCurrency), selectedCurrency)}
                    </div>
                    <div className="text-sm text-muted-foreground">RMSE</div>
                  </div>
                  <div className="text-center p-4 border rounded-lg">
                    <div className="text-2xl font-semibold text-accent">
                      {prediction.r2Score}
                    </div>
                    <div className="text-sm text-muted-foreground">R² Score</div>
                  </div>
                </div>

                <div className="text-sm text-muted-foreground">
                  <p className="mb-2"><strong>Random Forest Model Performance:</strong></p>
                  <ul className="space-y-1">
                    <li>• RMSE: {formatCurrency(convertPrice(prediction.rmse, selectedCurrency), selectedCurrency)} (Root Mean Square Error)</li>
                    <li>• R² Score: {prediction.r2Score} ({(prediction.r2Score * 100).toFixed(1)}% variance explained)</li>
                    <li>• Model trained on 50,000+ Indian car samples</li>
                    <li>• Features: Brand, Year, KM, Fuel, Location, Quality, CNG</li>
                    <li>• Prediction confidence: ±{formatCurrency(convertPrice(Math.round(prediction.rmse * 0.6), selectedCurrency), selectedCurrency)}</li>
                  </ul>
                </div>

              </div>
            ) : (
              <div className="text-center py-12 text-muted-foreground">
                <Car className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <p>Enter car details and click "Predict Price" to see the estimated value</p>
                {errorMessage && (
                  <p className="mt-2 text-red-600 text-sm">{errorMessage}{apiUrlUsed ? ` (API: ${apiUrlUsed})` : ''}</p>
                )}
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Price Comparison Resources Section */}
      {prediction && (
        <Card className="shadow-card mt-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <ExternalLink className="h-5 w-5" />
              Compare Prices on Top Platforms
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="grid grid-cols-1 gap-3">
                {carPriceResources.map((resource, index) => (
                  <div key={resource.name} className={`flex items-center justify-between p-3 border rounded-lg transition-colors ${
                    resource.isMain 
                      ? 'bg-gradient-to-r from-blue-50 to-indigo-50 border-blue-200 hover:from-blue-100 hover:to-indigo-100' 
                      : 'bg-muted/30 hover:bg-muted/50'
                  }`}>
                    <div className="flex items-center gap-3">
                      <div className="text-2xl">{resource.icon}</div>
                      <div className="flex-1">
                        <div className="flex items-center gap-2">
                          <h4 className={`font-semibold text-sm ${resource.isMain ? 'text-blue-800' : ''}`}>
                            {resource.name}
                            {resource.isMain && (
                              <Badge variant="default" className="ml-2 text-xs px-2 py-0.5 bg-blue-600">
                                Recommended
                              </Badge>
                            )}
                          </h4>
                          <div className="flex items-center gap-1">
                            <Star className="h-3 w-3 fill-yellow-400 text-yellow-400" />
                            <span className="text-xs text-muted-foreground">{resource.rating}</span>
                          </div>
                        </div>
                        <p className="text-xs text-muted-foreground">{resource.description}</p>
                        <div className="flex flex-wrap gap-1 mt-1">
                          {resource.features.slice(0, 3).map((feature, idx) => (
                            <Badge key={idx} variant={resource.isMain ? "default" : "secondary"} className={`text-xs px-2 py-0.5 ${
                              resource.isMain ? 'bg-blue-100 text-blue-800' : ''
                            }`}>
                              {feature}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    </div>
                    <a
                      href={resource.searchUrl(carData.brand, carData.model)}
                      target="_blank"
                      rel="noopener noreferrer"
                      className={`flex items-center gap-1 px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                        resource.isMain 
                          ? 'bg-blue-600 text-white hover:bg-blue-700' 
                          : 'bg-primary text-primary-foreground hover:bg-primary/90'
                      }`}
                      title={resource.name === "CarDekho" ? `View ${carData.brand} ${carData.model} model page on CarDekho` : `Search for ${carData.brand} ${carData.model} on ${resource.name}`}
                    >
                      {resource.isMain ? 'Search Now' : (resource.name === "CarDekho" ? 'View Model' : 'Search')}
                      <ExternalLink className="h-3 w-3" />
                    </a>
                  </div>
                ))}
              </div>
              <div className="text-xs text-muted-foreground bg-blue-50 p-3 rounded-lg">
                <div className="flex items-start gap-2">
                  <Shield className="h-4 w-4 text-blue-600 mt-0.5" />
                  <div>
                    <p className="font-medium text-blue-800">Pro Tip:</p>
                    <p>Start with <strong>OLX Autos</strong> for the best local deals and direct seller contact. <strong>CarDekho</strong> takes you directly to the specific {carData.brand} {carData.model} model page with detailed specifications. Then compare with Cars24 for instant valuations.</p>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};