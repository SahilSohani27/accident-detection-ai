import { Video, Cpu, CheckCircle, MessageSquare, Send } from 'lucide-react';

const ArchitectureSection = () => {
  return (
    <section className="py-24 bg-secondary/30">
      <div className="container px-4">
        <div className="max-w-5xl mx-auto">
          {/* Section header */}
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              System <span className="text-emergency">Architecture</span>
            </h2>
            <p className="text-muted-foreground text-lg">
              End-to-end pipeline for intelligent accident detection
            </p>
          </div>

          {/* Architecture diagram */}
          <div className="relative bg-card rounded-2xl border border-border p-8 overflow-hidden">
            {/* Background pattern */}
            <div className="absolute inset-0 opacity-5">
              <div className="absolute inset-0" style={{
                backgroundImage: 'radial-gradient(circle at 2px 2px, currentColor 1px, transparent 0)',
                backgroundSize: '24px 24px'
              }} />
            </div>

            {/* Flow diagram */}
            <div className="relative z-10">
              <div className="flex flex-col lg:flex-row items-center justify-between gap-6">
                {/* Video Input */}
                <div className="flex flex-col items-center text-center p-4 rounded-xl bg-secondary/50 min-w-[140px]">
                  <Video className="w-10 h-10 text-muted-foreground mb-2" />
                  <span className="text-sm font-medium">Video Input</span>
                  <span className="text-xs text-muted-foreground">CCTV / Dashcam</span>
                </div>

                <div className="hidden lg:block text-muted-foreground/50">→</div>

                {/* YOLOv8 Detection */}
                <div className="flex flex-col items-center text-center p-4 rounded-xl bg-emergency/10 border border-emergency/30 min-w-[140px]">
                  <Cpu className="w-10 h-10 text-emergency mb-2" />
                  <span className="text-sm font-medium">YOLOv8</span>
                  <span className="text-xs text-muted-foreground">Object Detection</span>
                </div>

                <div className="hidden lg:block text-muted-foreground/50">→</div>

                {/* Validation Layer */}
                <div className="flex flex-col items-center text-center p-4 rounded-xl bg-success/10 border border-success/30 min-w-[140px]">
                  <CheckCircle className="w-10 h-10 text-success mb-2" />
                  <span className="text-sm font-medium">Validation</span>
                  <span className="text-xs text-muted-foreground">Frame Streak Logic</span>
                </div>

                <div className="hidden lg:block text-muted-foreground/50">→</div>

                {/* SOS Generator */}
                <div className="flex flex-col items-center text-center p-4 rounded-xl bg-warning/10 border border-warning/30 min-w-[140px]">
                  <MessageSquare className="w-10 h-10 text-warning mb-2" />
                  <span className="text-sm font-medium">GPT SOS</span>
                  <span className="text-xs text-muted-foreground">Message Generator</span>
                </div>

                <div className="hidden lg:block text-muted-foreground/50">→</div>

                {/* Telegram Alert */}
                <div className="flex flex-col items-center text-center p-4 rounded-xl bg-blue-500/10 border border-blue-500/30 min-w-[140px]">
                  <Send className="w-10 h-10 text-blue-500 mb-2" />
                  <span className="text-sm font-medium">Telegram</span>
                  <span className="text-xs text-muted-foreground">Alert System</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ArchitectureSection;
