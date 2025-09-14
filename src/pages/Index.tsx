import { CarPricePredictor } from "@/components/CarPricePredictor";
import { DatasetVisualization } from "@/components/DatasetVisualization";
import { ThemeToggle } from "@/components/ThemeToggle";
import { Card, CardContent } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Brain, ChartBar, Database } from "lucide-react";
import heroImage from "@/assets/car-ml-hero.jpg";

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      {/* Theme Toggle - Fixed at top right */}
      <div className="fixed top-4 right-4 z-50">
        <ThemeToggle />
      </div>
      
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div 
          className="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-20"
          style={{ backgroundImage: `url(${heroImage})` }}
        />
        <div className="absolute inset-0 bg-gradient-hero opacity-90" />
        
        <div className="relative container mx-auto px-4 py-24">
          <div className="text-center text-white space-y-6">
            <h1 className="text-5xl md:text-6xl font-bold">
              Car Price Prediction
              <span className="block text-primary-glow">Machine Learning</span>
            </h1>
            <p className="text-xl md:text-2xl text-gray-200 max-w-3xl mx-auto">
              Advanced regression model trained on automotive data to predict accurate selling prices 
              using brand, year, mileage, and technical specifications
            </p>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-12 max-w-4xl mx-auto">
              <Card className="bg-white/10 backdrop-blur border-white/20">
                <CardContent className="p-6 text-center">
                  <Brain className="h-12 w-12 mx-auto mb-4 text-primary-glow" />
                  <h3 className="text-lg font-semibold mb-2">Regression Analysis</h3>
                  <p className="text-sm text-gray-200">
                    Random Forest & Linear Regression algorithms for accurate price predictions
                  </p>
                </CardContent>
              </Card>
              
              <Card className="bg-white/10 backdrop-blur border-white/20">
                <CardContent className="p-6 text-center">
                  <ChartBar className="h-12 w-12 mx-auto mb-4 text-primary-glow" />
                  <h3 className="text-lg font-semibold mb-2">Performance Metrics</h3>
                  <p className="text-sm text-gray-200">
                    RMSE evaluation and R² score tracking for model validation
                  </p>
                </CardContent>
              </Card>
              
              <Card className="bg-white/10 backdrop-blur border-white/20">
                <CardContent className="p-6 text-center">
                  <Database className="h-12 w-12 mx-auto mb-4 text-primary-glow" />
                  <h3 className="text-lg font-semibold mb-2">Rich Dataset</h3>
                  <p className="text-sm text-gray-200">
                    Comprehensive automotive data with multiple features and correlations
                  </p>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Main Content */}
      <section className="container mx-auto px-4 py-16">
        <Tabs defaultValue="predictor" className="w-full">
          <TabsList className="grid w-full grid-cols-2 max-w-md mx-auto mb-12">
            <TabsTrigger value="predictor" className="text-sm">Price Predictor</TabsTrigger>
            <TabsTrigger value="analysis" className="text-sm">Data Analysis</TabsTrigger>
          </TabsList>
          
          <TabsContent value="predictor" className="space-y-8">
            <CarPricePredictor />
          </TabsContent>
          
          <TabsContent value="analysis" className="space-y-8">
            <DatasetVisualization />
          </TabsContent>
        </Tabs>
      </section>
    </div>
  );
};

export default Index;
