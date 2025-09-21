import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { 
  Car, 
  Brain, 
  Target, 
  Users, 
  Award, 
  Github, 
  Mail, 
  MapPin,
  TrendingUp,
  Shield,
  Zap
} from "lucide-react";

export const Footer = () => {
  return (
    <footer className="bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      <div className="container mx-auto px-4 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          
          {/* About Us Section */}
          <div className="space-y-4">
            <div className="flex items-center gap-2 mb-4">
              <Car className="h-6 w-6 text-primary" />
              <h3 className="text-xl font-bold">About Us</h3>
            </div>
            <p className="text-gray-300 text-sm leading-relaxed">
              We're passionate about making car buying and selling transparent and fair. 
              Our AI-powered platform uses advanced machine learning to provide accurate 
              price predictions for the Indian automotive market.
            </p>
            <div className="flex items-center gap-2">
              <Badge variant="secondary" className="bg-primary/20 text-primary">
                <Brain className="h-3 w-3 mr-1" />
                AI-Powered
              </Badge>
              <Badge variant="secondary" className="bg-green-500/20 text-green-400">
                <Target className="h-3 w-3 mr-1" />
                91.96% Accuracy
              </Badge>
            </div>
          </div>

          {/* Our Mission */}
          <div className="space-y-4">
            <div className="flex items-center gap-2 mb-4">
              <Target className="h-6 w-6 text-primary" />
              <h3 className="text-xl font-bold">Our Mission</h3>
            </div>
            <ul className="space-y-3 text-sm text-gray-300">
              <li className="flex items-start gap-2">
                <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0" />
                <span>Democratize car pricing with transparent AI predictions</span>
              </li>
              <li className="flex items-start gap-2">
                <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0" />
                <span>Empower buyers and sellers with data-driven insights</span>
              </li>
              <li className="flex items-start gap-2">
                <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0" />
                <span>Bridge the gap between market value and asking price</span>
              </li>
              <li className="flex items-start gap-2">
                <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0" />
                <span>Make car transactions fair and informed</span>
              </li>
            </ul>
          </div>

          {/* Technology Stack */}
          <div className="space-y-4">
            <div className="flex items-center gap-2 mb-4">
              <Zap className="h-6 w-6 text-primary" />
              <h3 className="text-xl font-bold">Technology</h3>
            </div>
            <div className="space-y-3">
              <div className="flex items-center gap-2 text-sm">
                <div className="w-2 h-2 bg-blue-400 rounded-full" />
                <span className="text-gray-300">XGBoost Machine Learning</span>
              </div>
              <div className="flex items-center gap-2 text-sm">
                <div className="w-2 h-2 bg-green-400 rounded-full" />
                <span className="text-gray-300">React + TypeScript Frontend</span>
              </div>
              <div className="flex items-center gap-2 text-sm">
                <div className="w-2 h-2 bg-purple-400 rounded-full" />
                <span className="text-gray-300">FastAPI Backend</span>
              </div>
              <div className="flex items-center gap-2 text-sm">
                <div className="w-2 h-2 bg-orange-400 rounded-full" />
                <span className="text-gray-300">Python + scikit-learn</span>
              </div>
              <div className="flex items-center gap-2 text-sm">
                <div className="w-2 h-2 bg-pink-400 rounded-full" />
                <span className="text-gray-300">50,000+ Car Samples</span>
              </div>
            </div>
          </div>

          {/* Contact & Links */}
          <div className="space-y-4">
            <div className="flex items-center gap-2 mb-4">
              <Users className="h-6 w-6 text-primary" />
              <h3 className="text-xl font-bold">Connect</h3>
            </div>
            <div className="space-y-3 text-sm">
              <div className="flex items-center gap-2 text-gray-300">
                <Mail className="h-4 w-4 text-primary" />
                <span>contact@carpriceai.com</span>
              </div>
              <div className="flex items-center gap-2 text-gray-300">
                <MapPin className="h-4 w-4 text-primary" />
                <span>India - Pan India Service</span>
              </div>
              <div className="flex items-center gap-2 text-gray-300">
                <Github className="h-4 w-4 text-primary" />
                <a href="#" className="hover:text-primary transition-colors">
                  GitHub Repository
                </a>
              </div>
            </div>
            
            <div className="pt-4">
              <div className="flex items-center gap-2 text-xs text-gray-400">
                <Shield className="h-3 w-3" />
                <span>Secure • Reliable • Transparent</span>
              </div>
            </div>
          </div>
        </div>

        {/* Performance Metrics */}
        <Card className="mt-12 bg-gradient-to-r from-primary/10 to-blue-500/10 border-primary/20">
          <CardContent className="p-6">
            <div className="text-center mb-4">
              <h4 className="text-lg font-semibold text-white mb-2">Model Performance</h4>
              <p className="text-sm text-gray-300">Our XGBoost model delivers industry-leading accuracy</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="text-2xl font-bold text-primary mb-1">91.96%</div>
                <div className="text-sm text-gray-300">R² Score</div>
                <div className="text-xs text-gray-400">Variance Explained</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-400 mb-1">₹1.3L</div>
                <div className="text-sm text-gray-300">RMSE</div>
                <div className="text-xs text-gray-400">Average Error</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-400 mb-1">50K+</div>
                <div className="text-sm text-gray-300">Samples</div>
                <div className="text-xs text-gray-400">Training Data</div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Bottom Bar */}
        <div className="mt-12 pt-8 border-t border-gray-700">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="flex items-center gap-2 text-sm text-gray-400">
              <Car className="h-4 w-4" />
              <span>© 2024 Car Price AI. All rights reserved.</span>
            </div>
            <div className="flex items-center gap-6 text-sm text-gray-400">
              <a href="#" className="hover:text-primary transition-colors">Privacy Policy</a>
              <a href="#" className="hover:text-primary transition-colors">Terms of Service</a>
              <a href="#" className="hover:text-primary transition-colors">API Docs</a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

