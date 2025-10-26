import { Link } from "react-router-dom";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { AlertTriangle, Shield, Info } from "lucide-react";

export const LegalDisclaimer = () => {
  return (
    <div className="space-y-4">
      {/* Main Disclaimer */}
      <Alert className="border-amber-200 bg-amber-50">
        <AlertTriangle className="h-4 w-4 text-amber-600" />
        <AlertDescription className="text-sm">
          <strong>Important Disclaimer:</strong> Price predictions are estimates based on historical data and machine learning models. 
          Actual car prices may vary due to market conditions, vehicle condition, location, and other factors. 
          Always verify prices through multiple sources before making financial decisions.
        </AlertDescription>
      </Alert>

      {/* Terms and Conditions Notice */}
      <Alert className="border-blue-200 bg-blue-50">
        <Info className="h-4 w-4 text-blue-600" />
        <AlertDescription className="text-sm">
          By using this service, you agree to our{" "}
          <Link 
            to="/terms-and-conditions" 
            className="text-blue-600 hover:text-blue-800 underline font-medium"
          >
            Terms and Conditions
          </Link>{" "}
          and{" "}
          <Link 
            to="/privacy-policy" 
            className="text-blue-600 hover:text-blue-800 underline font-medium"
          >
            Privacy Policy
          </Link>
          . This service is for informational purposes only and does not constitute financial advice.
        </AlertDescription>
      </Alert>

      {/* Model Performance Notice */}
      <Alert className="border-green-200 bg-green-50">
        <Shield className="h-4 w-4 text-green-600" />
        <AlertDescription className="text-sm">
          <strong>Model Performance:</strong> Our XGBoost model achieves 91.96% accuracy (R² score) with an average error of ₹1.3 Lakh (RMSE). 
          Predictions are based on 50,000+ Indian car samples and include confidence levels. 
          No personal data is collected or stored.
        </AlertDescription>
      </Alert>
    </div>
  );
};

export const LegalFooter = () => {
  return (
    <div className="text-xs text-muted-foreground space-y-2 pt-4 border-t">
      <div className="flex flex-wrap gap-4 justify-center">
        <Link 
          to="/terms-and-conditions" 
          className="hover:text-primary transition-colors"
        >
          Terms & Conditions
        </Link>
        <Link 
          to="/privacy-policy" 
          className="hover:text-primary transition-colors"
        >
          Privacy Policy
        </Link>
        <span>© 2024 Car Price AI. All rights reserved.</span>
      </div>
      <div className="text-center">
        <p>
          <strong>Disclaimer:</strong> Price predictions are estimates only. 
          Always consult multiple sources and professional appraisers before making vehicle purchase decisions.
        </p>
      </div>
    </div>
  );
};



