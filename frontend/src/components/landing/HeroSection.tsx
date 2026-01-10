import { useNavigate } from 'react-router-dom';
import { AlertTriangle, Zap, Shield } from 'lucide-react';
import { Button } from '@/components/ui/button';

const HeroSection = () => {
  const navigate = useNavigate();

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-background via-background to-secondary/20" />
      
      {/* Animated glow effects */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-emergency/10 rounded-full blur-3xl animate-pulse" />
      <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-emergency/5 rounded-full blur-3xl animate-pulse delay-1000" />
      
      <div className="container relative z-10 px-4 py-20">
        <div className="max-w-4xl mx-auto text-center space-y-8">
          {/* Emergency badge */}
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-emergency/10 border border-emergency/30 animate-fade-in">
            <AlertTriangle className="w-4 h-4 text-emergency" />
            <span className="text-sm font-medium text-emergency">AI-Powered Emergency Response</span>
          </div>

          {/* Main title */}
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold tracking-tight animate-slide-up">
            <span className="text-gradient-emergency">🚨 ResQ Vision</span>
            <br />
            <span className="text-5xl text-foreground">AI Powered Accident Detection </span>
            <br />
            <span className="text-5xl text-foreground">& Emergency Alert System</span>
          </h1>

          {/* Subtitle */}
          <p className="text-lg md:text-xl text-muted-foreground max-w-3xl mx-auto animate-fade-in" style={{ animationDelay: '0.2s' }}>
          YOLOv8 + GPT powered system that operates on real-time RTSP/RTP camera feeds to detect road accidents and instantly alert nearby emergency response centers.
          This website is a simulation interface showcasing the backend AI pipeline and alerting workflow used in real-world deployment.
          </p>

          {/* Features highlights */}
          <div className="flex flex-wrap justify-center gap-4 text-sm text-muted-foreground animate-fade-in" style={{ animationDelay: '0.3s' }}>
            <div className="flex items-center gap-2">
              <Zap className="w-4 h-4 text-emergency" />
              <span>Real-time Detection</span>
            </div>
            <div className="flex items-center gap-2">
              <Shield className="w-4 h-4 text-success" />
              <span>False Positive Reduction</span>
            </div>
            <div className="flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-warning" />
              <span>Instant Alerts</span>
            </div>
          </div>

          {/* CTA Button */}
          <div className="pt-4 animate-fade-in" style={{ animationDelay: '0.4s' }}>
            <Button 
              size="lg" 
              onClick={() => navigate('/demo')}
              className="text-lg px-8 py-6 bg-emergency hover:bg-emergency/90 text-emergency-foreground glow-emergency transition-all duration-300 hover:scale-105"
            >
              Try ResQ Vision
              <Zap className="w-5 h-5 ml-2" />
            </Button>
          </div>
        </div>
      </div>

      {/* Bottom gradient fade */}
      <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-background to-transparent" />
    </section>
  );
};

export default HeroSection;
