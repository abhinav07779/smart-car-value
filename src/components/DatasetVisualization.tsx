import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ScatterChart, Scatter, BarChart, Bar } from "recharts";
import { Database, BarChart3, Activity, Globe } from "lucide-react";
import { formatCurrency, convertPrice } from "@/utils/currency";

// Mock dataset for visualization with multi-currency support (prices in INR)
const mockDataset = [
  { brand: "Toyota", model: "Camry", year: 2020, mileage: 45000, fuelType: "Petrol", transmission: "Automatic", engineSize: 2.5, price: 2100000 },
  { brand: "Honda", model: "Civic", year: 2019, mileage: 52000, fuelType: "Petrol", transmission: "Manual", engineSize: 2.0, price: 1680000 },
  { brand: "BMW", model: "X3", year: 2021, mileage: 35000, fuelType: "Petrol", transmission: "Automatic", engineSize: 3.0, price: 3300000 },
  { brand: "Mercedes", model: "C-Class", year: 2020, mileage: 40000, fuelType: "Petrol", transmission: "Automatic", engineSize: 2.0, price: 3100000 },
  { brand: "Audi", model: "A4", year: 2019, mileage: 48000, fuelType: "Petrol", transmission: "Automatic", engineSize: 2.0, price: 2850000 },
  { brand: "Ford", model: "Focus", year: 2018, mileage: 65000, fuelType: "Petrol", transmission: "Manual", engineSize: 1.6, price: 1360000 },
];

// Currency-aware data for charts
const getMultiCurrencyData = (inrData: Array<{ avgPrice: number }>, currency: string = 'INR') => {
  return inrData.map(item => ({
    ...item,
    avgPrice: currency === 'INR' ? item.avgPrice : convertPrice(item.avgPrice, currency)
  }));
};

const priceByYearData = [
  { year: 2018, avgPrice: 1650000 },
  { year: 2019, avgPrice: 2100000 },
  { year: 2020, avgPrice: 2580000 },
  { year: 2021, avgPrice: 3100000 },
  { year: 2022, avgPrice: 3550000 },
  { year: 2023, avgPrice: 3880000 },
];

const priceByBrandData = [
  { brand: "Mercedes", avgPrice: 3550000 },
  { brand: "BMW", avgPrice: 3400000 },
  { brand: "Audi", avgPrice: 3150000 },
  { brand: "Toyota", avgPrice: 2350000 },
  { brand: "Honda", avgPrice: 2100000 },
  { brand: "Ford", avgPrice: 1780000 },
];

const mileageVsPriceData = mockDataset.map(car => ({
  mileage: car.mileage / 1000, // Convert to thousands
  price: car.price / 1000, // Convert to thousands
  brand: car.brand
}));

export const DatasetVisualization = () => {
  const [selectedCurrency, setSelectedCurrency] = useState('INR');
  
  // Get currency-converted data
  const priceByYearConverted = getMultiCurrencyData(priceByYearData, selectedCurrency);
  const priceByBrandConverted = getMultiCurrencyData(priceByBrandData, selectedCurrency);

  return (
    <div className="w-full max-w-6xl mx-auto space-y-8">
      {/* Currency Selector */}
      <Card className="shadow-card">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Globe className="h-5 w-5" />
            Currency Settings
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center gap-4">
            <label className="text-sm font-medium">Display prices in:</label>
            <select 
              value={selectedCurrency}
              onChange={(e) => setSelectedCurrency(e.target.value)}
              className="px-3 py-2 border rounded-md bg-background"
            >
              <option value="INR">INR (₹)</option>
              <option value="USD">USD ($)</option>
              <option value="EUR">EUR (€)</option>
              <option value="GBP">GBP (£)</option>
              <option value="JPY">JPY (¥)</option>
              <option value="CAD">CAD (C$)</option>
              <option value="AUD">AUD (A$)</option>
            </select>
          </div>
        </CardContent>
      </Card>

      {/* Dataset Overview */}
      <Card className="shadow-card">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Database className="h-5 w-5" />
            Training Dataset Overview
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div className="text-center p-4 bg-gradient-card rounded-lg">
              <div className="text-2xl font-bold text-primary">1,247</div>
              <div className="text-sm text-muted-foreground">Total Records</div>
            </div>
            <div className="text-center p-4 bg-gradient-card rounded-lg">
              <div className="text-2xl font-bold text-primary">7</div>
              <div className="text-sm text-muted-foreground">Features</div>
            </div>
            <div className="text-center p-4 bg-gradient-card rounded-lg">
              <div className="text-2xl font-bold text-primary">85.6%</div>
              <div className="text-sm text-muted-foreground">Training Accuracy</div>
            </div>
            <div className="text-center p-4 bg-gradient-card rounded-lg">
              <div className="text-2xl font-bold text-primary">
                {formatCurrency(convertPrice(210000, selectedCurrency), selectedCurrency)}
              </div>
              <div className="text-sm text-muted-foreground">Avg RMSE</div>
            </div>
          </div>

          {/* Sample Data Table */}
          <div className="overflow-x-auto">
            <div className="text-sm font-medium mb-2">Sample Training Data:</div>
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b">
                  <th className="text-left p-2">Brand</th>
                  <th className="text-left p-2">Model</th>
                  <th className="text-left p-2">Year</th>
                  <th className="text-left p-2">Mileage</th>
                  <th className="text-left p-2">Fuel</th>
                  <th className="text-left p-2">Engine</th>
                  <th className="text-left p-2">Price ({selectedCurrency})</th>
                </tr>
              </thead>
              <tbody>
                {mockDataset.slice(0, 4).map((car, index) => (
                  <tr key={index} className="border-b">
                    <td className="p-2">{car.brand}</td>
                    <td className="p-2">{car.model}</td>
                    <td className="p-2">{car.year}</td>
                    <td className="p-2">{car.mileage.toLocaleString()}km</td>
                    <td className="p-2">
                      <Badge variant="outline" className="text-xs">{car.fuelType}</Badge>
                    </td>
                    <td className="p-2">{car.engineSize}L</td>
                    <td className="p-2 font-medium">
                      {formatCurrency(convertPrice(car.price, selectedCurrency), selectedCurrency)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      {/* Visualizations */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Price by Year Trend */}
        <Card className="shadow-card">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BarChart3 className="h-5 w-5" />
              Price Trends by Year
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={priceByYearConverted}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="year" />
                <YAxis />
                <Tooltip formatter={(value) => [formatCurrency(value as number, selectedCurrency), "Avg Price"]} />
                <Line 
                  type="monotone" 
                  dataKey="avgPrice" 
                  stroke="hsl(var(--primary))" 
                  strokeWidth={3}
                  dot={{ fill: "hsl(var(--primary))", strokeWidth: 2, r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Price by Brand */}
        <Card className="shadow-card">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BarChart3 className="h-5 w-5" />
              Average Price by Brand
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={priceByBrandConverted}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="brand" />
                <YAxis />
                <Tooltip formatter={(value) => [formatCurrency(value as number, selectedCurrency), "Avg Price"]} />
                <Bar 
                  dataKey="avgPrice" 
                  fill="hsl(var(--accent))"
                  radius={[4, 4, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Mileage vs Price Scatter Plot */}
        <Card className="shadow-card lg:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Activity className="h-5 w-5" />
              Mileage vs Price Correlation
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={350}>
              <ScatterChart data={mileageVsPriceData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="mileage" 
                  name="Mileage"
                  label={{ value: 'Mileage (thousands km)', position: 'insideBottom', offset: -5 }}
                />
                <YAxis 
                  dataKey="price" 
                  name="Price"
                  label={{ value: 'Price (thousands ₹)', angle: -90, position: 'insideLeft' }}
                />
                <Tooltip 
                  cursor={{ strokeDasharray: '3 3' }}
                  formatter={(value, name) => [
                    name === 'price' ? formatCurrency((value as number) * 1000, selectedCurrency) : `${value}k km`,
                    name === 'price' ? 'Price' : 'Mileage'
                  ]}
                  labelFormatter={(label) => ''}
                />
                <Scatter 
                  dataKey="price" 
                  fill="hsl(var(--primary-glow))"
                  fillOpacity={0.7}
                />
              </ScatterChart>
            </ResponsiveContainer>
            <div className="mt-4 text-sm text-muted-foreground">
              <p><strong>Correlation Analysis:</strong> The scatter plot shows a negative correlation between mileage and price, 
              indicating that cars with higher mileage tend to have lower selling prices, as expected.</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};