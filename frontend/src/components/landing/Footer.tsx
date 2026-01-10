import { QRCodeSVG } from 'qrcode.react';
import { ExternalLink, Linkedin, Github } from 'lucide-react';

const TELEGRAM_LINK = 'https://t.me/+aQKM_C_puyIwNzBl';
const GITHUB_REPO = 'https://github.com/SahilSohani27/accident-detection-ai'; // Update with your GitHub repo URL

const Footer = () => {
  return (
    <footer className="py-16 bg-secondary/30 border-t border-border">
      <div className="container px-4">
        <div className="max-w-4xl mx-auto">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            {/* Left side - Info */}
            <div className="text-center md:text-left">
              <h3 className="text-2xl font-bold mb-4">
                🚨 AI Accident Detection System
              </h3>
              <p className="text-muted-foreground mb-6">
                A backend-focused AI system demonstration showcasing real-time 
                accident detection and emergency response capabilities.
              </p>
              
              <div className="space-y-3 text-md">
                <p className="font-medium text-foreground">Contributors</p>
                <div className="space-y-2">
                  <a
                    href="https://www.linkedin.com/in/sahilsohani/" // Update with actual LinkedIn URL
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-2 text-muted-foreground hover:text-emergency transition-colors"
                  >
                    <Linkedin className="w-4 h-4" />
                    <span>Sahil Sohani</span>
                    <ExternalLink className="w-3 h-3" />
                  </a>
                  <a
                    href="https://www.linkedin.com/in/dushyant-atalkar-50281028a/" // Update with actual LinkedIn URL
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-2 text-muted-foreground hover:text-emergency transition-colors"
                  >
                    <Linkedin className="w-4 h-4" />
                    <span>Dushyant Atalkar</span>
                    <ExternalLink className="w-3 h-3" />
                  </a>
                </div>
                <div className="pt-2">
                  <a
                    href={GITHUB_REPO}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-2 text-muted-foreground hover:text-emergency transition-colors"
                  >
                    <Github className="w-4 h-4" />
                    <span>View on GitHub</span>
                    <ExternalLink className="w-3 h-3" />
                  </a>
                </div>
                <p className="text-muted-foreground pt-2">Built with an "AI For All" initiative</p>
              </div>
            </div>

            {/* Right side - QR Code */}
            <div className="flex flex-col items-center">
              <div className="p-4 rounded-2xl bg-card border border-border">
                <div className="p-3 bg-foreground rounded-xl">
                  <QRCodeSVG
                    value={TELEGRAM_LINK}
                    size={140}
                    bgColor="hsl(0, 0%, 95%)"
                    fgColor="hsl(0, 0%, 10%)"
                    level="H"
                    includeMargin={false}
                  />
                </div>
              </div>
              
              <p className="mt-4 text-sm text-muted-foreground text-center">
                Scan to join our Telegram Alert Group
              </p>
              
              <a
                href={TELEGRAM_LINK}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-3 inline-flex items-center gap-2 text-sm text-emergency hover:text-emergency/80 transition-colors"
              >
                <span>Join Telegram Channel</span>
                <ExternalLink className="w-4 h-4" />
              </a>
            </div>
          </div>

          {/* Bottom */}
          <div className="mt-12 pt-8 border-t border-border text-center text-sm text-muted-foreground">
            <p>© 2026 ResQ Vision. All rights reserved.</p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
