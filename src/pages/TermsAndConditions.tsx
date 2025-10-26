import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowLeft, AlertTriangle, Shield, Info } from "lucide-react";
import { Link } from "react-router-dom";

export const TermsAndConditions = () => {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center gap-4 mb-6">
          <Link to="/">
            <Button variant="outline" size="sm">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to App
            </Button>
          </Link>
          <div>
            <h1 className="text-3xl font-bold text-primary">Terms and Conditions</h1>
            <p className="text-muted-foreground">Last Updated: December 2024</p>
          </div>
        </div>

        {/* Important Notice */}
        <Card className="mb-6 border-blue-200 bg-blue-50 dark:border-blue-800 dark:bg-blue-950/30">
          <CardContent className="p-6">
            <div className="flex items-start gap-3">
              <AlertTriangle className="h-5 w-5 text-blue-600 dark:text-blue-400 mt-0.5" />
              <div>
                <h3 className="font-semibold text-blue-800 dark:text-blue-300 mb-2">Important Notice</h3>
                <p className="text-blue-700 dark:text-blue-400">
                  By using our Car Price Prediction AI service, you agree to these terms. 
                  Please read them carefully before using our service.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <div className="max-w-4xl space-y-6">
          {/* Section 1: Acceptance of Terms */}
          <Card>
            <CardHeader>
              <CardTitle className="text-xl">1. Acceptance of Terms</CardTitle>
            </CardHeader>
            <CardContent>
              <p>
                By accessing and using the Car Price Prediction AI service ("Service"), you accept and agree to be bound by the terms and provision of this agreement. If you do not agree to abide by the above, please do not use this service.
              </p>
            </CardContent>
          </Card>

          {/* Section 2: Description of Service */}
          <Card>
            <CardHeader>
              <CardTitle className="text-xl">2. Description of Service</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="mb-4">
                Car Price Prediction AI is a machine learning-powered web application that provides estimated car prices for used vehicles in the Indian automotive market. The service uses:
              </p>
              <ul className="list-disc pl-6 space-y-2">
                <li><strong>XGBoost Machine Learning Model</strong> with 91.96% accuracy</li>
                <li><strong>50,000+ car samples</strong> from Indian automotive data</li>
                <li><strong>Real-time price predictions</strong> based on vehicle specifications</li>
                <li><strong>Multi-currency support</strong> for price display</li>
                <li><strong>Data visualization</strong> and market analysis tools</li>
              </ul>
            </CardContent>
          </Card>

          {/* Section 3: Price Predictions and Accuracy */}
          <Card>
            <CardHeader>
              <CardTitle className="text-xl">3. Price Predictions and Accuracy</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <h4 className="font-semibold mb-2">3.1 Prediction Nature</h4>
                <ul className="list-disc pl-6 space-y-1">
                  <li><strong>Estimates Only:</strong> All price predictions are estimates based on historical data</li>
                  <li><strong>No Guarantees:</strong> We do not guarantee the accuracy of any price prediction</li>
                  <li><strong>Market Variables:</strong> Actual car prices may vary due to market conditions, location, condition, and other factors</li>
                </ul>
              </div>
              <div>
                <h4 className="font-semibold mb-2">3.2 Model Performance</h4>
                <ul className="list-disc pl-6 space-y-1">
                  <li><strong>R² Score:</strong> 91.96% (variance explained by the model)</li>
                  <li><strong>RMSE:</strong> ₹1.3 Lakh average error</li>
                  <li><strong>Training Data:</strong> 50,000+ Indian car samples</li>
                  <li><strong>Confidence Levels:</strong> Predictions include confidence percentages</li>
                </ul>
              </div>
            </CardContent>
          </Card>

          {/* Section 4: User Responsibilities */}
          <Card>
            <CardHeader>
              <CardTitle className="text-xl">4. User Responsibilities</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <h4 className="font-semibold mb-2">4.1 Accurate Information</h4>
                <ul className="list-disc pl-6 space-y-1">
                  <li>You must provide accurate and truthful information about the vehicle</li>
                  <li>False or misleading information may result in inaccurate predictions</li>
                  <li>You are responsible for verifying all input data before submission</li>
                </ul>
              </div>
              <div>
                <h4 className="font-semibold mb-2">4.2 Permitted Use</h4>
                <ul className="list-disc pl-6 space-y-1">
                  <li>Use the service for personal, non-commercial purposes only</li>
                  <li>Do not attempt to reverse engineer or extract the machine learning model</li>
                  <li>Do not use automated systems to access the service without permission</li>
                  <li>Respect rate limits and fair usage policies</li>
                </ul>
              </div>
            </CardContent>
          </Card>

          {/* Section 5: Disclaimers and Limitations */}
          <Card>
            <CardHeader>
              <CardTitle className="text-xl">5. Disclaimers and Limitations</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <h4 className="font-semibold mb-2">5.1 Service Availability</h4>
                <ul className="list-disc pl-6 space-y-1">
                  <li><strong>"As Is" Basis:</strong> The service is provided "as is" without warranties</li>
                  <li><strong>No Guarantees:</strong> We do not guarantee uninterrupted service availability</li>
                  <li><strong>Maintenance:</strong> Service may be temporarily unavailable for maintenance</li>
                </ul>
              </div>
              <div>
                <h4 className="font-semibold mb-2">5.2 Price Prediction Disclaimers</h4>
                <ul className="list-disc pl-6 space-y-1">
                  <li><strong>Not Financial Advice:</strong> Price predictions are not financial or investment advice</li>
                  <li><strong>No Liability:</strong> We are not liable for decisions made based on predictions</li>
                  <li><strong>Market Risk:</strong> Car prices are subject to market fluctuations and risks</li>
                  <li><strong>Verification Required:</strong> Always verify prices through multiple sources</li>
                </ul>
              </div>
            </CardContent>
          </Card>

          {/* Section 6: Limitation of Liability */}
          <Card>
            <CardHeader>
              <CardTitle className="text-xl">6. Limitation of Liability</CardTitle>
            </CardHeader>
            <CardContent>
              <p>
                We are not liable for any financial losses resulting from price predictions. Users assume all risk when making decisions based on predictions. No compensation for inaccurate predictions or market changes.
              </p>
            </CardContent>
          </Card>

          {/* Section 7: Data and Privacy */}
          <Card>
            <CardHeader>
              <CardTitle className="text-xl">7. Data and Privacy</CardTitle>
            </CardHeader>
            <CardContent>
              <p>
                We collect only vehicle specifications you provide. No personal information is collected or stored. Data is used solely for price prediction calculations and may be used to improve the machine learning model. Please see our{" "}
                <Link to="/privacy-policy" className="text-primary hover:underline">
                  Privacy Policy
                </Link>{" "}
                for more details.
              </p>
            </CardContent>
          </Card>

          {/* Section 8: Intellectual Property */}
          <Card>
            <CardHeader>
              <CardTitle className="text-xl">8. Intellectual Property</CardTitle>
            </CardHeader>
            <CardContent>
              <p>
                The Car Price Prediction AI service and all its components are proprietary. Machine learning models, algorithms, and datasets are protected intellectual property. You retain ownership of any data you input.
              </p>
            </CardContent>
          </Card>

          {/* Section 9: Termination */}
          <Card>
            <CardHeader>
              <CardTitle className="text-xl">9. Termination</CardTitle>
            </CardHeader>
            <CardContent>
              <p>
                You may stop using the service at any time. We may terminate or suspend the service at any time. We may modify or discontinue features without notice.
              </p>
            </CardContent>
          </Card>

          {/* Section 10: Modifications */}
          <Card>
            <CardHeader>
              <CardTitle className="text-xl">10. Modifications</CardTitle>
            </CardHeader>
            <CardContent>
              <p>
                We may update these terms at any time. Updated terms will be posted on the service. Continued use constitutes acceptance of new terms.
              </p>
            </CardContent>
          </Card>

          {/* Section 11: Governing Law */}
          <Card>
            <CardHeader>
              <CardTitle className="text-xl">11. Governing Law</CardTitle>
            </CardHeader>
            <CardContent>
              <p>
                These terms are governed by Indian law. Any disputes will be resolved in Indian courts. Users agree to submit to Indian jurisdiction.
              </p>
            </CardContent>
          </Card>

          {/* Contact Information */}
          <Card className="border-emerald-200 bg-emerald-50 dark:border-emerald-800 dark:bg-emerald-950/30">
            <CardHeader>
              <CardTitle className="text-xl flex items-center gap-2">
                <Info className="h-5 w-5 text-emerald-600 dark:text-emerald-400" />
                12. Contact Information
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="mb-4 dark:text-emerald-400">For questions about these Terms and Conditions, please contact:</p>
              <ul className="list-disc pl-6 space-y-1 dark:text-emerald-400">
                <li><strong>Email:</strong> contact@carpriceai.com</li>
                <li><strong>Service:</strong> Car Price Prediction AI</li>
              </ul>
            </CardContent>
          </Card>

          {/* Important Notice */}
          <Card className="border-purple-200 bg-purple-50 dark:border-purple-800 dark:bg-purple-950/30">
            <CardContent className="p-6">
              <div className="flex items-start gap-3">
                <AlertTriangle className="h-5 w-5 text-purple-600 dark:text-purple-400 mt-0.5" />
                <div>
                  <h3 className="font-semibold text-purple-800 dark:text-purple-300 mb-2">Important Notice</h3>
                  <p className="text-purple-700 dark:text-purple-400">
                    This service provides price estimates only. Always consult multiple sources and professional appraisers before making significant financial decisions related to vehicle purchases or sales.
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Footer */}
          <div className="text-center text-sm text-muted-foreground pt-6 border-t">
            <p><strong>Last Updated:</strong> December 2024 | <strong>Version:</strong> 1.0</p>
            <p>© 2024 Car Price AI. All rights reserved.</p>
          </div>
        </div>
      </div>
    </div>
  );
};



